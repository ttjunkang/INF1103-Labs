import json
import os

from inventory import Inventory
from supplier import Supplier
from product import Product
from order import Order
from product_factory import ProductFactory
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


INVENTORY_FILE = "inventory.json"

UNKNOWN_SUPPLIER = {"id": "S000", "name": "Unknown Supplier", "contact_email": "-"}

DISCOUNT_OPTIONS: dict[str, tuple[str, DiscountStrategy]] = {
    "1": ("No discount", NoDiscount()),
    "2": ("10% off", PercentageDiscount(10)),
    "3": ("$20 off orders of $200 or more", BulkDiscount(200, 20)),
    "4": ("Student discount (5% off)", StudentDiscount()),
}


# Input helpers
def get_valid_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0:
                print("Error: Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")


def get_valid_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Error: Please enter a valid whole number.")
            continue
        return int(raw)


def get_valid_choice(prompt: str, options: list[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Error: Please enter one of: {', '.join(options)}.")


# 1 Supplier object is shared by all its products
def collect_suppliers(inventory: Inventory) -> dict[str, Supplier]:
    suppliers: dict[str, Supplier] = {}
    for product in inventory.get_products():
        supplier = product.get_supplier()
        suppliers[supplier.get_supplier_id()] = supplier
    return suppliers

 
def get_or_create_supplier(data: dict[str, str], suppliers: dict[str, Supplier]) -> Supplier:
    supplier_id = data["id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]


# Uses the saved "type" to create the correct subclass
# The factory uses the saved "type" to create the correct subclass
def create_product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    supplier = get_or_create_supplier(item.get("supplier", UNKNOWN_SUPPLIER), suppliers)
    product_type = item.get("type", "physical")  # Lab 6 data has no type
    return ProductFactory.create(product_type, item["id"], item["name"], item["price"], item["stock"], supplier,weight=item.get("weight", 0.0), download_size=item.get("download_size", 0.0))


# File handling
def load_inventory() -> Inventory:
    inventory = Inventory()
 
    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return inventory
 
    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        suppliers: dict[str, Supplier] = {}
        for item in data:
            inventory.add_product(create_product_from_dict(item, suppliers))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("Could not read existing file. Starting with an empty inventory.")
        inventory = Inventory()
 
    return inventory


def save_inventory(inventory: Inventory) -> None:
    print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
    print()


# Menu actions which talk to the Inventory object not raw data
def choose_supplier(inventory: Inventory) -> Supplier:
    suppliers = collect_suppliers(inventory)
    if suppliers:
        print("Existing suppliers:")
        for supplier in suppliers.values():
            supplier.display_information()
 
    supplier_id = input("Supplier ID: ").strip()
    if supplier_id in suppliers:
        print(f"Using existing supplier: {suppliers[supplier_id].get_name()}")
        return suppliers[supplier_id]
 
    print("New supplier - please enter the details.")
    name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, contact_email)


def add_product_menu(inventory: Inventory) -> None:
    print("Add New Product")
    product_id = input("Product ID: ").strip()
 
    if inventory.find_product(product_id) is not None:
        print(f"A product with ID {product_id} already exists.")
        print()
        return
 
    name = input("Product Name: ").strip()
    price = get_valid_float("Price: ")
    stock = get_valid_int("Stock Quantity: ")
    supplier = choose_supplier(inventory)
 
    print("Product Type: 1. Physical  2. Digital")
    product_type = get_valid_choice("Choose type (1/2): ", ["1", "2"])
 
    # Collects the details meaning the factory creates the object
    if product_type == "1":
        weight = get_valid_float("Weight (kg): ")
        product = ProductFactory.create("physical", product_id, name, price, stock, supplier, weight=weight)
    else:
        download_size = get_valid_float("Download Size (MB): ")
        product = ProductFactory.create("digital", product_id, name, price, stock, supplier, download_size=download_size)
 
    inventory.add_product(product)
    print("Product added successfully!")
    print()


def update_stock_menu(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    print()
 
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        print()
        return
 
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    print()
 
    new_stock = get_valid_int("New Stock Quantity: ")
    print()
    if product.update_stock(new_stock):
        print("Stock updated successfully!")
    else:
        print("Error: Invalid stock quantity.")
    print()


def search_product_menu(inventory: Inventory) -> None:
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    print()
 
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        print()
        return
 
    print("Product Found")
    print("-" * 70)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print("    ", end="")
    product.get_supplier().display_information()
    print("-" * 70)
    print()


def remove_product_menu(inventory: Inventory) -> None:
    print("Remove Product")
    product_id = input("Enter Product ID: ").strip()
    print()
 
    removed_product = inventory.remove_product(product_id)
    if removed_product is None:
        print("Product not found.")
    else:
        print(f"{removed_product.get_name()} removed from the inventory.")
        print("The Product object still exists:")
        removed_product.display_information()
    print()


def create_order_menu(inventory: Inventory) -> None:
    print("Create Order")
    order = Order(input("Order ID: ").strip())
 
    while True:
        product_id = input("Product ID to order (or 'done'): ").strip()
        if product_id.lower() == "done":
            break
 
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
 
        quantity = get_valid_int("Quantity: ")
        if quantity == 0:
            print("Error: Quantity must be at least 1.")
            continue
 
        order.add_order_line(product, quantity)
        print(f"Added {quantity} x {product.get_name()}.")

    if order.get_order_lines():
        print()
        order.set_discount(choose_discount())

    print()
    order.display_order()


# Picks a strategy object, order never needs to know which one 
def choose_discount() -> DiscountStrategy:
    print("Discount Options:")
    for option, (label, _) in DISCOUNT_OPTIONS.items():
        print(f"{option}. {label}")
    choice = get_valid_choice("Choose discount (1-4): ", list(DISCOUNT_OPTIONS.keys()))
    return DISCOUNT_OPTIONS[choice][1]

 
def print_menu() -> None:
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
 
    inventory = load_inventory()
    if inventory.is_empty():
        tech_supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.com")
        soft_supplier = Supplier("S002", "SoftHub Pte Ltd", "orders@softhub.com")
        inventory.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15, tech_supplier, weight=2.5))
        inventory.add_product(ProductFactory.create("physical", "P002", "Mouse", 25.50, 40, tech_supplier, weight=0.2))
        inventory.add_product(ProductFactory.create("digital", "D001", "Operating System", 129.00, 50, soft_supplier, download_size=4500.0))
 
    while True:
        print_menu()
        choice = input("Enter option: ").strip()
        print()
 
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            remove_product_menu(inventory)
        elif choice == "6":
            create_order_menu(inventory)
        elif choice == "7":
            save_inventory(inventory)
        elif choice == "8":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose a number from 1-8.")

 
 
if __name__ == "__main__":
    main()