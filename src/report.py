from abc import ABC, abstractmethod

class Report(ABC):
    """
    Abstract base class for executive reports in the EcoWatch system.
    Each report must implement the generate method.
    """
    @abstractmethod
    def generate(self, logs):
        """
        Generate the report based on the provided logs.

        Args:
            logs (list): List of Log objects to process.
        Returns:
            Any: The result of the report generation (format depends on the report type).
        """
        pass
