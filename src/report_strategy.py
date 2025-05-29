from abc import ABC, abstractmethod

class ReportStrategy(ABC):
    """
    Interface for report generation strategies.
    Implements the Strategy design pattern for flexible report logic.
    """
    @abstractmethod
    def generate(self, logs):
        """
        Generate a report based on the provided logs.

        Args:
            logs (list): List of Log objects to process.
        Returns:
            Any: The result of the report generation (format depends on the strategy).
        """
        pass
