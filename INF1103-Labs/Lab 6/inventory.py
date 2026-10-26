class Inventory:
    """SRP: Manages a COLLECTION of Product objects."""
 
    def __init__(self):
        self.__products = []
 
    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True