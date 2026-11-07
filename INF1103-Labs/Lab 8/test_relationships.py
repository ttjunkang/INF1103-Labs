from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
 
 
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

def test_aggregation() -> None:
    print("=== 3. Aggregation: Inventory and Product ===")
    supplier = Supplier("S200", "TechWorld Pte Ltd", "sales@techworld.com")
 
    # 1. Product exists BEFORE any Inventory
    laptop = PhysicalProduct("P200", "Laptop", 1200.00, 10, supplier, 2.5)
    inventory_a = Inventory()
    inventory_b = Inventory()
 
    # 2. Add to Inventory A
    inventory_a.add_product(laptop)
    print(f"Laptop in Inventory A? {inventory_a.find_product('P200') is not None}")
 
    # 3. Remove from Inventory A (Predict first: does the laptop still work?)
    removed = inventory_a.remove_product("P200")
    print(f"Laptop in Inventory A after remove? {inventory_a.find_product('P200') is not None}")
    print(f"Removed object is the same laptop? {removed is laptop}")
    print("Laptop still works after removal:")
    laptop.display_information()
 
    # 4. Add the SAME object to Inventory B (transfer)
    inventory_b.add_product(laptop)
    print(f"Same laptop now in Inventory B? {inventory_b.find_product('P200') is laptop}")
 
    # 5. Emptying an Inventory does not destroy the Product
    print(f"Inventory A empty? {inventory_a.is_empty()} - laptop still exists: {laptop.get_name()}")
    print()
 
 
 
if __name__ == "__main__":
    test_aggregation()