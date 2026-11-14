import inspect
import unittest

from supplier import Supplier
from order import Order
from product_factory import ProductFactory
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


def make_order(order_id: str, discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S900", "Test Supplier", "test@supplier.com")
    chair = ProductFactory.create("physical", "P900", "Chair", 100.00, 10, supplier, weight=5.0)
    ebook = ProductFactory.create("digital", "D900", "eBook", 50.00, 10, supplier, download_size=2.0)
    order = Order(order_id, discount)
    order.add_order_line(chair, 2)
    order.add_order_line(ebook, 1)
    return order


class TestDiscounts(unittest.TestCase):

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount_takes_percentage_off(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_applies_at_or_above_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertAlmostEqual(bulk.apply(250.0), 230.0)
        self.assertAlmostEqual(bulk.apply(200.0), 180.0)

    def test_bulk_discount_not_applied_below_threshold(self) -> None:
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_student_discount_takes_five_percent_off(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(100.0), 95.0)

    def test_invalid_discount_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(200, -20)

    def test_abstract_strategy_cannot_be_created(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy() 

    def test_order_without_strategy_uses_no_discount(self) -> None:
        order = make_order("O001")
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_calculate_total_goes_through_strategy(self) -> None:
        order = make_order("O002", BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_subtotal(), 250.0)
        self.assertAlmostEqual(order.calculate_total(), 230.0)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = make_order("O003", BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        order = make_order("O004", StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_order_has_no_discount_if_elif_logic(self) -> None:
        self.assertNotRegex(inspect.getsource(Order.calculate_total), r"\bif\b")
        self.assertNotIn("elif", inspect.getsource(Order))

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        order_a = make_order("O005", shared)
        order_b = make_order("O006", shared)
        self.assertIs(order_a.get_discount(), order_b.get_discount())
        self.assertAlmostEqual(order_b.calculate_total(), 225.0)


if __name__ == "__main__":
    unittest.main()