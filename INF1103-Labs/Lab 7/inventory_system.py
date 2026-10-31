import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

INVENTORY_FILE = "inventory.json"


# Input helpers (main program is responsible for user input)
def get_valid_float(prompt):
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


def get_valid_int(prompt):
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Error: Please enter a valid whole number.")
            continue
        return int(raw)


def get_valid_choice(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Error: Please enter one of: {', '.join(options)}.")


# Uses the saved "type" to create the correct subclass
def create_product_from_dict(item):
    product_type = item.get("type", "physical")  # Lab 6 data has no type
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item.get("download_size", 0.0))
    return PhysicalProduct(item["id"], item["name"], item["price"],
                           item["stock"], item.get("weight", 0.0))


# File handling
def load_inventory():
    inventory = Inventory()

    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return inventory

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(create_product_from_dict(item))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        print("Could not read existing file. Starting with an empty inventory.")
        inventory = Inventory()

    return inventory


def save_inventory(inventory):
    print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
    print()


# Menu actions (talk to the Inventory object, not raw data)
def add_product_menu(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print(f"A product with ID {product_id} already exists.")
        print()
        return

    name = input("Product Name: ").strip()
    price = get_valid_float("Price: ")
    stock = get_valid_int("Stock Quantity: ")

    print("Product Type: 1. Physical  2. Digital")
    product_type = get_valid_choice("Choose type (1/2): ", ["1", "2"])

    if product_type == "1":
        weight = get_valid_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_valid_float("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print("Product added successfully!")
    print()


def update_stock_menu(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    print()

    product = inventory.search_product(product_id)
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


def search_product_menu(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    print()

    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        print()
        return

    print("Product Found")
    print("-" * 50)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print("-" * 50)
    print()


def print_menu():
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = load_inventory()
    if inventory.is_empty():
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.2))
        inventory.add_product(DigitalProduct("D001", "Operating System", 129.00, 50, 4500.0))

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
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose a number from 1-6.")


if __name__ == "__main__":
    main()