from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    # Interface for any class that can be shipped must be able to calculate its shipping cost

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass