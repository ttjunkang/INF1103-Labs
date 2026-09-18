def get_valid_input():
    entry = input("Enter stock quantity (or 'quit' to finish): ")

    if entry == "quit":
        return "quit"

    if not entry.isdigit():
        print("Error: Invalid input. Please enter a whole number.")
        return None

    entry = int(entry)

    if entry < 0:
        print("Error: Stock quantity cannot be negative.")
        return None

    return entry


def calculate_tax(amount):
    tax_rate = 0.10
    return amount * tax_rate


def process_delivery(current_total, new_value):
    return current_total + new_value


# Quick test
if __name__ == "__main__":
    result = get_valid_input()
    print("You got back:", result)

    tax = calculate_tax(100)
    print("Tax on 100:", tax)

    new_total = process_delivery(50, 20)
    print("New total after adding 20 to 50:", new_total)