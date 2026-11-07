from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    # SRP: Represents and manages 1 product
 
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier 

    # Getters - read only access from outside
    def get_supplier(self) -> Supplier:
        return self.__supplier
    
    def get_product_id(self) -> str:
        return self.__product_id
 
    def get_name(self) -> str:
        return self.__name
 
    def get_price(self) -> float:
        return self.__price
 
    def get_stock(self) -> int:
        return self.__stock

    # Product controls how its own stock is changed
    def update_stock(self, quantity: int) -> bool:
        if not isinstance(quantity, int) or quantity < 0:
            return False
        self.__stock = quantity
        return True

    # Abstract method: every child class must implement this
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
 
    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
            f"Supplier: {self.__supplier.get_name()}"
        )

     # Converts product to a dictionary for JSON
    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }