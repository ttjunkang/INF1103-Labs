from digital_product import DigitalProduct
from physical_product import PhysicalProduct

print("=== Physical product ===")
guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, 3.5)
guitar.display_information()
print()

print("=== Digital product ===")
os_software = DigitalProduct("D100", "Operating System", 129.00, 50, 4500.0)
os_software.display_information()
print()