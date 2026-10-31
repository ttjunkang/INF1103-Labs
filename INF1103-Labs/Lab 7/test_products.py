from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product


print("=== Physical product ===")
guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, 3.5)
guitar.display_information()
print()

print("=== Digital product ===")
os_software = DigitalProduct("D100", "Operating System", 129.00, 50, 4500.0)
os_software.display_information()
print()

print("=== Fulfilment info (abstract method) ===")
print(f"{guitar.get_name()}: {guitar.get_fulfilment_info()}")
print(f"{os_software.get_name()}: {os_software.get_fulfilment_info()}")
print()

print("=== Create a Product directly ===")
try:
    Product("X001", "Generic", 10.00, 1)
except TypeError as error:
    print(f"TypeError: {error}")
print()