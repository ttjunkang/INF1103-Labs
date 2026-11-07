from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
 
 
# Section 2: Association - Supplier and Product
def test_association() -> None:
    print("=== 2. Association: Supplier and Product ===")
    supplier = Supplier("S100", "Music Supplies Co", "hello@musicsupplies.com")
    guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, supplier, 3.5)
    ebook = DigitalProduct("D100", "Guitar eBook", 19.99, 50, supplier, 12.5)
 
    print("Supplier through each Product:")
    guitar.get_supplier().display_information()
    ebook.get_supplier().display_information()
    print(f"Supplier is a separate object from the products? {supplier is not guitar and supplier is not ebook}")
    print(f"Both products refer to the SAME Supplier object? {guitar.get_supplier() is ebook.get_supplier()}")
 
    # Predict first: can each Product still show its supplier after this?
    del supplier
    print("After 'del supplier':")
    guitar.get_supplier().display_information()
    ebook.get_supplier().display_information()
 
    # A Supplier can also exist with no Products at all
    new_supplier = Supplier("S101", "Brand New Supplier", "hi@newsupplier.com")
    print("Supplier with no products:")
    new_supplier.display_information()
    print()
 
 
if __name__ == "__main__":
    test_association()