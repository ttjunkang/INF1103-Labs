inventory = 0
failed_entries = 0

while True:
    entry = input("Enter stock quantity (or 'quit' to finish): ")

    if entry == "quit":
        break

    if not entry.isdigit():
        print("Error: Invalid input. Please enter a whole number.")
        failed_entries += 1
        continue  

    entry = int(entry)

    if entry < 0:
        print("Error: Stock quantity cannot be negative.")
        failed_entries += 1
        continue
