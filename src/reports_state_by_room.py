from src.report import Report
from src.report_strategy import ReportStrategy
import pandas as pd

class StateByRoomStrategy(ReportStrategy):
    """
    Strategy for generating a state-by-room report.
    Aggregates environmental data by room.
    """
    def generate(self, logs):
        """
        Generate a summary report by room.

        Args:
            logs (list): List of Log objects to process.
        Returns:
            pd.DataFrame: Tabular summary by room.
        """
        data = [
            {
                "room": log.sala,
                "temperature": log.temperatura,
                "humidity": log.humedad,
                "co2": log.co2,
                "state": log.estado,
                "timestamp": log.timestamp,
            }
            for log in logs
        ]
        df = pd.DataFrame(data)
        if df.empty:
            return df
        summary = df.groupby("room").agg({
            "temperature": "mean",
            "humidity": "mean",
            "co2": "mean",
            "state": lambda x: x.mode()[0] if not x.mode().empty else None,
        }).reset_index()
        return summary

class StateByRoomReport(Report):
    """
    Report that summarizes the environmental state by room using a strategy.
    """
    def __init__(self, strategy=None):
        """
        Initialize the report with a strategy.

        Args:
            strategy (ReportStrategy, optional): The strategy to use for report generation.
        """
        self.strategy = strategy or StateByRoomStrategy()

    def generate(self, logs):
        """
        Generate the report using the assigned strategy.

        Args:
            logs (list): List of Log objects to process.
        Returns:
            pd.DataFrame: The generated report as a DataFrame.
        """
        return self.strategy.generate(logs)
