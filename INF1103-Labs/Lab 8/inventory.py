
from product import Product


class Inventory:
    # SRP: Manages a collection of Product objects
 
    def __init__(self) -> None:
        # Typed with the base class, so it can hold ANY kind of Product
        self.__products: list[Product] = []
 
    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def get_products(self) -> list[Product]:
        return list(self.__products)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 70)
        if not self.__products:
            print("(No products in inventory)")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 70)
        print()
 
    def is_empty(self) -> bool:
        return len(self.__products) == 0
 
    # Returns list of dictionaries for JSON
    def to_list(self) -> list[dict[str, object]]:
        return [product.to_dict() for product in self.__products]
 