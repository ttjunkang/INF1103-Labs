import json
import os

INVENTORY_FILE = "inventory.json"


#Helper functions
def find_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None

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

#Display of Products and Adding Product
def display_all(inventory):
    print("Current Inventory")
    print("-" * 50)
    if not inventory:
        print("(No products in inventory)")
    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
            )
    print("-" * 50)
    print()

def add_product(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()

    if find_product(inventory, product_id) is not None:
        print(f"A product with ID {product_id} already exists.")
        print()
        return

    name = input("Product Name: ").strip()
    price = get_valid_float("Price: ")
    stock = get_valid_int("Stock Quantity: ")

    product = {
        "id": product_id, 
        "name": name, 
        "price": price, 
        "stock": stock
    }

    inventory.append(product)
    print("Product added successfully!")
    print()

#Update Stock and Search Product
def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    print()

    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        print()
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    print()

    new_stock = get_valid_int("New Stock Quantity: ")
    print()
    product["stock"] = new_stock
    print("Stock updated successfully!")
    print()

def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    print()

    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        print()
        return

    print("Product Found")
    print("-" * 50)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 50)
    print()

#Load Inventory
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
            print("Inventory loaded successfully.")
            return data
        except (json.JSONDecodeError, OSError):
            print("Could not read existing file. Starting with an empty inventory.")
            return []
    else:
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return []

#Save Inventory
def save_inventory(inventory):
    print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)
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
    if not inventory:
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
        ]

    while True:
        print_menu()
        choice = input("Enter option: ").strip()
        print()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
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