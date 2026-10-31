from product import Product


class PhysicalProduct(Product):
    """A physical product IS-A Product, with a weight."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    # Overriding: parent shows common info, child adds weight
    def display_information(self):
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg")

    # Overriding: parent fields + type and weight
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data