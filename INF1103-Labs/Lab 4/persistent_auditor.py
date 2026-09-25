INVENTORY_FILE = "inventory.txt"

def load_inventory():
    orders = []
    history = []
    total = 0
 
    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        # No prior data yet - start fresh.
        return orders, history, total
 
    section = None
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
 
        if line == "[ORDERS]":
            section = "orders"
            continue
        elif line == "[HISTORY]":
            section = "history"
            continue
        elif line.startswith("[TOTAL]"):
            section = "total"
            continue
 
        if section == "orders":
            # Format: id,name,qty
            parts = line.split(",")
            if len(parts) == 3:
                order_id, name, qty = parts
                orders.append({
                    "id": int(order_id),
                    "name": name,
                    "qty": int(qty)
                })
        elif section == "history":
            history.append(int(line))
        elif section == "total":
            total = int(line)
 
    return orders, history, total

def save_inventory(orders, history, total):
    with open(INVENTORY_FILE, "w") as f:
        f.write("[ORDERS]\n")
        for order in orders:
            f.write(f"{order['id']},{order['name']},{order['qty']}\n")
 
        f.write("[HISTORY]\n")
        for amount in history:
            f.write(f"{amount}\n")
 
        f.write("[TOTAL]\n")
        f.write(f"{total}\n")
 
    print(f"Order successfully saved to {INVENTORY_FILE}")
    
def get_valid_input():
    entry = input("Enter stock quantity (or 'quit' to finish): ")

    if entry == "quit":
        return "quit"

    if not entry.isdigit():
        print("Error: Invalid input. Please enter a whole number.")
        return None

    quantity = int(entry)

    if quantity < 0:
        print("Error: Stock quantity cannot be negative.")
        return None

    return quantity


def calculate_tax(amount):
    tax_rate = 0.10
    return amount * tax_rate


def process_delivery(current_total, new_value):
    return current_total + new_value


def generate_report(total_units, failed_attempts):
    print("\n--- Inventory Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def main():
    total_inventory, transaction_history = load_inventory(INVENTORY_FILE)

    print("=== Persistent Auditor ===")
    print(f"Loaded inventory: {total_inventory}")
    print(f"Loaded history: {transaction_history}\n")
    
    total_deliveries_processed = 0
    failed_entries = 0
    total_tax_collected = 0.0


    while True:
        result = get_valid_input()

        if result == "quit":
            break

        if result is None:
            failed_entries += 1
            continue

        quantity = result

        transaction_history.append(quantity)   # <-- new line     

        total_inventory = process_delivery(total_inventory, quantity)
        tax_for_this_delivery = calculate_tax(quantity)
        total_tax_collected += tax_for_this_delivery
        total_deliveries_processed += 1

        print(
            f"Accepted: +{quantity} units (tax: {tax_for_this_delivery:.2f}). "
            f"Current inventory: {total_inventory}"
        )

    save_inventory(INVENTORY_FILE, total_inventory, transaction_history)
    generate_report(total_deliveries_processed, failed_entries)
    print(f"Total Tax Collected: {total_tax_collected:.2f}")


if __name__ == "__main__":
    main()