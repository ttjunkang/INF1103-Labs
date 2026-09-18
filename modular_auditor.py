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


# Quick test - call it once and see what comes back
if __name__ == "__main__":
    result = get_valid_input()
    print("You got back:", result)