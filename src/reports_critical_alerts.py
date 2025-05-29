from src.report import Report
from src.report_strategy import ReportStrategy
import pandas as pd

class CriticalAlertsStrategy(ReportStrategy):
    """
    Strategy for generating a critical alerts report.
    Identifies logs where environmental metrics exceed critical thresholds.
    """
    # Example thresholds (can be adjusted)
    TEMP_THRESHOLD = 30.0
    HUMIDITY_THRESHOLD = 80.0
    CO2_THRESHOLD = 1000.0

    def generate(self, logs):
        """
        Generate a report of critical alerts based on thresholds.

        Args:
            logs (list): List of Log objects to process.
        Returns:
            pd.DataFrame: DataFrame of critical alerts.
        """
        data = [
            {
                "room": log.sala,
                "temperature": log.temperatura,
                "humidity": log.humedad,
                "co2": log.co2,
                "state": log.estado,
                "timestamp": log.timestamp,
                "message": log.mensaje,
            }
            for log in logs
            if (
                log.temperatura > self.TEMP_THRESHOLD or
                log.humedad > self.HUMIDITY_THRESHOLD or
                log.co2 > self.CO2_THRESHOLD
            )
        ]
        return pd.DataFrame(data)

class CriticalAlertsReport(Report):
    """
    Report that lists all critical environmental alerts using a strategy.
    """
    def __init__(self, strategy=None):
        """
        Initialize the report with a strategy.

        Args:
            strategy (ReportStrategy, optional): The strategy to use for report generation.
        """
        self.strategy = strategy or CriticalAlertsStrategy()

    def generate(self, logs):
        """
        Generate the report using the assigned strategy.

        Args:
            logs (list): List of Log objects to process.
        Returns:
            pd.DataFrame: The generated report as a DataFrame.
        """
        return self.strategy.generate(logs)
