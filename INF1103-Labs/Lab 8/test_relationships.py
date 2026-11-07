from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
 
 
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
 
    del supplier
    print("After 'del supplier':")
    guitar.get_supplier().display_information()
    ebook.get_supplier().display_information()
 
    new_supplier = Supplier("S101", "Brand New Supplier", "hi@newsupplier.com")
    print("Supplier with no products:")
    new_supplier.display_information()
    print()


def test_aggregation() -> None:
    print("=== 3. Aggregation: Inventory and Product ===")
    supplier = Supplier("S200", "TechWorld Pte Ltd", "sales@techworld.com")
 
    laptop = PhysicalProduct("P200", "Laptop", 1200.00, 10, supplier, 2.5)
    inventory_a = Inventory()
    inventory_b = Inventory()
 
    inventory_a.add_product(laptop)
    print(f"Laptop in Inventory A? {inventory_a.find_product('P200') is not None}")
 
    removed = inventory_a.remove_product("P200")
    print(f"Laptop in Inventory A after remove? {inventory_a.find_product('P200') is not None}")
    print(f"Removed object is the same laptop? {removed is laptop}")
    print("Laptop still works after removal:")
    laptop.display_information()
 
    inventory_b.add_product(laptop)
    print(f"Same laptop now in Inventory B? {inventory_b.find_product('P200') is laptop}")
 
    print(f"Inventory A empty? {inventory_a.is_empty()} - laptop still exists: {laptop.get_name()}")
    print()


def test_composition() -> None:
    print("=== 4. Composition: Order and OrderLine ===")
    supplier = Supplier("S300", "TechWorld Pte Ltd", "sales@techworld.com")
    laptop = PhysicalProduct("P300", "Laptop", 1200.00, 10, supplier, 2.5)
    mouse = PhysicalProduct("P301", "Mouse", 25.50, 40, supplier, 0.2)
    antivirus = DigitalProduct("D300", "Antivirus Software", 49.90, 100, supplier, 350.0)
 
    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(mouse, 2)
    order_1.add_order_line(antivirus, 1)
    order_1.display_order()
 
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 3)
    order_2.display_order()
 
    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"Same OrderLine object in both orders? {line_1 is line_2}")
    print(f"Same Product object in both lines?    {line_1.get_product() is line_2.get_product()}")
    print(f"OrderLine ids: {id(line_1)} vs {id(line_2)}")
    print(f"Product ids:   {id(line_1.get_product())} vs {id(line_2.get_product())}")
    print()
 
    order_1.remove_order_line("P301")
    print("After removing the mouse line from O001:")
    order_1.display_order()


 
if __name__ == "__main__":
    test_composition()