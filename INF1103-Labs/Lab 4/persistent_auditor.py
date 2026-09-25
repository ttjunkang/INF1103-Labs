INVENTORY_FILE = "inventory.txt"

def load_inventory(filename):
    total = 0
    history = []

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("TOTAL:"):
                    total = int(line.replace("TOTAL:", ""))
                elif line.startswith("HISTORY:"):
                    raw = line.replace("HISTORY:", "")
                    if raw:
                        history = [int(x) for x in raw.split(",")]

    except FileNotFoundError:
        print(f"No existing '{filename}' found. Starting with a fresh inventory.")
        total = 1
        history = []

    return total, history

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

        total_inventory = process_delivery(total_inventory, quantity)
        tax_for_this_delivery = calculate_tax(quantity)
        total_tax_collected += tax_for_this_delivery
        total_deliveries_processed += 1

        print(
            f"Accepted: +{quantity} units (tax: {tax_for_this_delivery:.2f}). "
            f"Current inventory: {total_inventory}"
        )

    generate_report(total_deliveries_processed, failed_entries)
    print(f"Total Tax Collected: {total_tax_collected:.2f}")


if __name__ == "__main__":
    main()