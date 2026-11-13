from product import Product
from order_line import OrderLine
 
 
class Order:
    #Composition whole: an Order creates and owns its OrderLine objects
 
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
 
    def get_order_id(self) -> str:
        return self.__order_id
 
    # Copy of the list
    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)
 
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
 
    # Asks each OrderLine for subtotal
    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total
 
    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        print("-" * 70)
        if not self.__order_lines:
            print("(No order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 70)
        print(f"Total: ${self.calculate_total():.2f}")
        print()