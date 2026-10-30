class Inventory:
    """SRP: Manages a COLLECTION of Product objects."""
 
    def __init__(self):
        self.__products = []
 
    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("-" * 50)
        if not self.__products:
            print("(No products in inventory)")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 50)
        print()
 
    def is_empty(self):
        return len(self.__products) == 0
 
    # Returns list of dictionaries (used when saving to JSON)
    def to_list(self):
        return [product.to_dict() for product in self.__products]
 