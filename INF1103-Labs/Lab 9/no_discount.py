from discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    # Default strategy: the total stays the same

    def apply(self, total: float) -> float:
        return total