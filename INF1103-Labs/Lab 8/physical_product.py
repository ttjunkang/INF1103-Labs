from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A physical product IS-A Product (inheritance)
    and CanBeShipped (interface)."""

    BASE_SHIPPING_COST = 5.00
    SHIPPING_RATE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    # Required by the abstract Product class
    def get_fulfilment_info(self):
        return "Requires physical shipping"

    # Overriding: parent shows common info, child adds weight
    def display_information(self):
        super().display_information()
        print(
            f"    Weight: {self.__weight:.2f} kg | "
            f"Shipping Cost: ${self.calculate_shipping_cost():.2f}"
        )

    # Overriding: parent fields + type and weight
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
    
    # Required by the CanBeShipped interface
    def calculate_shipping_cost(self):
        return PhysicalProduct.BASE_SHIPPING_COST + self.__weight * PhysicalProduct.SHIPPING_RATE_PER_KG