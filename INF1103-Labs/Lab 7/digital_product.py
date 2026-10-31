from product import Product


class DigitalProduct(Product):
    """A digital product IS-A Product, with a download size."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size
    
    # Overriding: parent shows common info, child adds download size
    def display_information(self):
        super().display_information()
        print(f"    Download Size: {self.__download_size:.1f} MB")

    # Overriding: parent fields + type and download size
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data