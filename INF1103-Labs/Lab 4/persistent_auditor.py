INVENTORY_FILE = "inventory.txt"


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

def load_inventory():
    total_inventory = 0
    total_tax_collected = 0.0
    history = []
 
    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return total_inventory, total_tax_collected, history
 
    section = None
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
 
        if line == "[TOTAL_INVENTORY]":
            section = "total_inventory"
            continue
        elif line == "[TOTAL_TAX]":
            section = "total_tax"
            continue
        elif line == "[HISTORY]":
            section = "history"
            continue
 
        if section == "total_inventory":
            total_inventory = int(line)
        elif section == "total_tax":
            total_tax_collected = float(line)
        elif section == "history":
            history.append(int(line))
 
    return total_inventory, total_tax_collected, history

def save_inventory(total_inventory, total_tax_collected, history):
    """
    Writes the final running total, total tax collected, and the
    full transaction history list back to INVENTORY_FILE.
    """
    with open(INVENTORY_FILE, "w") as f:
        f.write("[TOTAL_INVENTORY]\n")
        f.write(f"{total_inventory}\n")
 
        f.write("[TOTAL_TAX]\n")
        f.write(f"{total_tax_collected}\n")
 
        f.write("[HISTORY]\n")
        for amount in history:
            f.write(f"{amount}\n")
 
    print(f"Inventory successfully saved to {INVENTORY_FILE}")


def main():
    total_inventory, total_tax_collected, history = load_inventory()
    
    total_deliveries_processed = 0
    failed_entries = 0

    if history:
        print(f"Loaded previous session: {len(history)} past deliveries, "
              f"current inventory = {total_inventory}, "
              f"tax collected so far = {total_tax_collected:.2f}")
 
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

        history.append(quantity)
 
        print(
            f"Accepted: +{quantity} units (tax: {tax_for_this_delivery:.2f}). "
            f"Current inventory: {total_inventory}"
        )
 
    generate_report(total_deliveries_processed, failed_entries)
    print(f"Total Tax Collected: {total_tax_collected:.2f}")
 

    save_inventory(total_inventory, total_tax_collected, history)


if __name__ == "__main__":
    main()