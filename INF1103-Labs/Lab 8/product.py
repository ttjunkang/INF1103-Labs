from abc import ABC, abstractmethod


class Product(ABC):
    """SRP: Represents and manages ONE product."""
 
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Getters (read-only access from outside)
    def get_product_id(self):
        return self.__product_id
 
    def get_name(self):
        return self.__name
 
    def get_price(self):
        return self.__price
 
    def get_stock(self):
        return self.__stock

    # Product controls how its own stock is changed
    def update_stock(self, quantity):
        if not isinstance(quantity, int) or quantity < 0:
            return False
        self.__stock = quantity
        return True

    # Abstract method: every child class MUST implement this
    @abstractmethod
    def get_fulfilment_info(self):
        pass
 
    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

     # Converts product to a dictionary (used when saving to JSON)
    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }