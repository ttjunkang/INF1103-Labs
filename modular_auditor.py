"""
Modular Inventory Auditor
--------------------------
Week 3 refactor of auditor.py. Same behaviour as before, but the logic is now
split into small, "pure" functions: each one takes input as parameters and
returns a result, instead of directly reading/writing variables that live
outside the function (global state). This makes each piece independently
testable and easy to extend later (e.g. adding discounts).
"""

inventory = 0