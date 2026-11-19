import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory
from inventory_system import get_positive_float, load_products, save_inventory

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_CSV = os.path.join(PROJECT_DIR, "products.csv")


class TestErrorHandling(unittest.TestCase):

    def setUp(self) -> None:
        self.inventory = Inventory()
        self.supplier = Supplier("S940", "CSV Supplier", "csv@supplier.com")

    def load(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_keeps_asking_until_value_is_valid(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output): value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_not_accepted(self) -> None:
        with patch("builtins.input", side_effect=["0", "5"]), redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_float("Price: "), 5.0)

    def test_valid_rows_load_and_bad_rows_are_skipped(self) -> None:
        lines = self.load(PRODUCTS_CSV)
        loaded_ids = [product.get_product_id() for product in self.inventory.get_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("could not convert string to float: 'abc'", lines[1])
        self.assertEqual(lines[-2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled_without_crashing(self) -> None:
        missing = os.path.join(tempfile.gettempdir(), "no_such_products_file.csv")
        lines = self.load(missing)
        self.assertEqual(lines, [f"Products file not found: {missing}", "Load attempt finished."])
        self.assertTrue(self.inventory.is_empty())

    def test_duplicate_product_ids_are_skipped(self) -> None:
        self.load(PRODUCTS_CSV)
        lines = self.load(PRODUCTS_CSV)
        self.assertIn("0 products loaded.", lines)
        self.assertEqual(len(self.inventory.get_products()), 3)

    def test_save_error_is_reported_not_raised(self) -> None:
        self.inventory.add_product(ProductFactory.create("physical", "P950", "Lamp", 10.00, 1, self.supplier))
        bad_path = os.path.join(tempfile.gettempdir(), "no_such_folder_lab9", "inventory.json")
        output = io.StringIO()
        with patch("inventory_system.INVENTORY_FILE", bad_path), redirect_stdout(output):
            save_inventory(self.inventory)
        self.assertIn("Could not save", output.getvalue())


if __name__ == "__main__":
    unittest.main()