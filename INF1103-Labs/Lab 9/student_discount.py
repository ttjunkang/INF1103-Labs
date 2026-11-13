from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):

    PERCENTAGE = 5.0

    def apply(self, total: float) -> float:
        return total * (100 - StudentDiscount.PERCENTAGE) / 100