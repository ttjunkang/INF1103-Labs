from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    # Digital product is a Product, with a download size

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    # Required by the abstract Product class
    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link"
    
    # Overriding: parent shows common info, child adds download size
    def display_information(self) -> None:
        super().display_information()
        print(f"    Download Size: {self.__download_size:.1f} MB")

    # Overriding: parent fields + type and download size
    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data