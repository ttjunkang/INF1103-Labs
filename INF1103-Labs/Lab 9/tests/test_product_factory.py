import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S910", "Factory Supplier", "factory@supplier.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P910", "Desk Lamp", 25.00, 10, self.supplier, weight=1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_name(), "Desk Lamp")

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D910", "Photo Editor", 49.90, 100, self.supplier, download_size=950.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_supplier(), self.supplier)

    def test_unknown_type_raises_value_error_with_clear_message(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S910", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_factory_products_are_used_through_product_type(self) -> None:
        products: list[Product] = [
            ProductFactory.create("physical", "P911", "Chair", 80.00, 5, self.supplier, weight=7.0),
            ProductFactory.create("digital", "D911", "Music Album", 9.90, 50, self.supplier, download_size=80.0),
        ]
        info = [product.get_fulfilment_info() for product in products]
        self.assertEqual(info, ["Requires physical shipping", "Delivered digitally via download link"])


if __name__ == "__main__":
    unittest.main()