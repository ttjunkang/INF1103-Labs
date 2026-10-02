import json
import os

INVENTORY_FILE = "inventory.json"

inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]

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


def add_product(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()

    if find_product(inventory, product_id) is not None:
        print(f"A product with ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    price = get_valid_float("Price: ")
    stock = get_valid_int("Stock Quantity: ")

    product = {"id": product_id, "name": name, "price": price, "stock": stock}
    inventory.append(product)
    print("Product added successfully!")

display_all(inventory)
add_product(inventory)
display_all(inventory)