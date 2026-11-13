from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    # Takes a fixed amount off any total at or above the threshold

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0 or amount < 0:
            raise ValueError("Threshold must be greater than zero and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total