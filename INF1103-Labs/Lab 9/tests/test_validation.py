import unittest

from supplier import Supplier
from order import Order
from order_line import OrderLine
from product_factory import ProductFactory


class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S920", "Validation Supplier", "check@supplier.com")
        self.product = ProductFactory.create("physical", "P930", "Mouse", 25.50, 40, self.supplier)

    def test_price_must_be_greater_than_zero(self) -> None:
        for bad_price in [0, -5.0]:
            with self.assertRaises(ValueError) as context:
                ProductFactory.create("physical", "P920", "Lamp", bad_price, 10, self.supplier)
            self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("digital", "D920", "App", 10.00, -1, self.supplier)
        self.assertEqual(str(context.exception), "Stock quantity cannot be negative.")

    def test_zero_stock_is_allowed(self) -> None:
        product = ProductFactory.create("physical", "P921", "Lamp", 10.00, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_every_product_type_follows_the_same_rules(self) -> None:
        for product_type in ["physical", "digital"]:
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "X920", "Item", -1.00, 1, self.supplier)
            product = ProductFactory.create(product_type, "X921", "Item", 5.00, 3, self.supplier)
            self.assertFalse(product.update_stock(-5))
            self.assertEqual(product.get_stock(), 3)

    def test_quantity_must_be_greater_than_zero(self) -> None:
        for bad_quantity in [0, -2]:
            with self.assertRaises(ValueError) as context:
                OrderLine(self.product, bad_quantity)
            self.assertEqual(str(context.exception), "Quantity must be greater than zero.")

    def test_order_rejects_bad_quantity_and_keeps_no_line(self) -> None:
        order = Order("O930")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)
        self.assertEqual(order.get_order_lines(), [])

    def test_valid_quantity_is_accepted(self) -> None:
        order_line = OrderLine(self.product, 2)
        self.assertAlmostEqual(order_line.calculate_subtotal(), 51.00)


if __name__ == "__main__":
    unittest.main()