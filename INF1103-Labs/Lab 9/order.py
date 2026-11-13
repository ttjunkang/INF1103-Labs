from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount


class Order:
    # Composition whole: an Order creates and owns its OrderLine objects
    # Association: an Order uses a DiscountStrategy but does not own it

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    # Copy of the list
    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    # The strategy can be swapped later without changing Order
    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    # Creates the OrderLine
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    # Lines are removed through the Order
    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    # Total before discount: asks each OrderLine for its subtotal
    def calculate_subtotal(self) -> float:
        return sum(order_line.calculate_subtotal() for order_line in self.__order_lines)

    # The strategy works out the discount, so Order has no discount checks
    def calculate_total(self) -> float:
        return self.__discount.apply(self.calculate_subtotal())

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        print("-" * 70)
        if not self.__order_lines:
            print("(No order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 70)
        subtotal = self.calculate_subtotal()
        total = self.calculate_total()
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: -${subtotal - total:.2f} ({type(self.__discount).__name__})")
        print(f"Total: ${total:.2f}")
        print()