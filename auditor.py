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