import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = "inventory.json"

# Input helpers (for user input)
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

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("Product added successfully!")
    print()

#Update Stock and Search Product
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
    print("-" * 50)
    print()

#Load Inventory (file handling)
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
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        print("Could not read existing file. Starting with an empty inventory.")
        inventory = Inventory()

    return inventory

#Save Inventory
def save_inventory(inventory):
    print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory.to_list(), f, indent=4)
    print(f"Inventory saved successfully to {INVENTORY_FILE}.")
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

#Menu and Main Function
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = load_inventory()
    if inventory.is_empty():
        inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
        inventory.add_product(Product("P002", "Mouse", 25.50, 40))
        inventory.add_product(Product("P003", "Keyboard", 45.00, 25))

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