from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface: any class that can be shipped MUST be able to calculate its shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass