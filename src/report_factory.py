from src.report import Report
from src.reports_state_by_room import StateByRoomReport
from src.reports_critical_alerts import CriticalAlertsReport
import pandas as pd

class ReportFactory:
    """
    Factory class to create report instances based on the report type.
    Implements the Factory design pattern for extensibility.
    """
    def __init__(self):
        self._creators = {}

    def register_report(self, report_type, creator):
        """
        Register a new report type with its creator function or class.

        Args:
            report_type (str): The identifier for the report type.
            creator (callable): The function or class to create the report instance.
        """
        self._creators[report_type] = creator

    def create_report(self, report_type, *args, **kwargs):
        """
        Create a report instance of the specified type.

        Args:
            report_type (str): The identifier for the report type.
        Returns:
            Report: An instance of a subclass of Report.
        Raises:
            ValueError: If the report type is not registered.
        """
        creator = self._creators.get(report_type)
        if not creator:
            raise ValueError(f"Report type '{report_type}' is not registered.")
        return creator(*args, **kwargs)

    def register_default_reports(self):
        """
        Register all default report types in the factory.
        """
        self.register_report("state_by_room", StateByRoomReport)
        self.register_report("critical_alerts", CriticalAlertsReport)


def export_report(df, filename):
    """
    Export a pandas DataFrame report to CSV or XLSX format automatically based on the file extension.

    Args:
        df (pd.DataFrame): The report data to export.
        filename (str): The output file path (.csv or .xlsx).
    """
    if filename.endswith('.csv'):
        df.to_csv(filename, index=False)
    elif filename.endswith('.xlsx'):
        df.to_excel(filename, index=False)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")
