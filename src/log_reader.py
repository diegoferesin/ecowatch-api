import pandas as pd
from datetime import datetime
from src.log import Log

# Decorator for logging execution of methods
def log_execution(func):
    """
    Decorator to log the execution of a function or method.
    """
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished {func.__name__}.")
        return result
    return wrapper

class LogReader:
    """
    Reads and validates environmental logs from various sources (e.g., CSV).
    Ensures each entry contains the required fields and correct data types.
    """
    REQUIRED_FIELDS = ["timestamp", "sala", "estado", "temperatura", "humedad", "co2"]

    def __init__(self, filepath):
        """
        Initialize the LogReader with the path to the log file.

        Args:
            filepath (str): Path to the log file (CSV).
        """
        self.filepath = filepath

    @log_execution
    def read_logs(self):
        """
        Read and validate logs from the CSV file.

        Returns:
            list: List of valid Log objects.
        """
        df = pd.read_csv(self.filepath)
        logs = []
        for _, row in df.iterrows():
            if not self._is_valid_row(row):
                continue
            try:
                log = Log(
                    timestamp=self._parse_timestamp(row["timestamp"]),
                    sala=row["sala"],
                    estado=row["estado"],
                    temperatura=float(row["temperatura"]),
                    humedad=float(row["humedad"]),
                    co2=float(row["co2"]),
                    mensaje=row.get("mensaje", None)
                )
                logs.append(log)
            except Exception:
                # Invalid data type or parsing error
                continue
        return logs

    def _is_valid_row(self, row):
        """
        Check if the row contains all required fields and non-null values.

        Args:
            row (pd.Series): The row to validate.
        Returns:
            bool: True if valid, False otherwise.
        """
        for field in self.REQUIRED_FIELDS:
            if field not in row or pd.isnull(row[field]):
                return False
        return True

    def _parse_timestamp(self, value):
        """
        Parse the timestamp string to a datetime object.

        Args:
            value (str): The timestamp string.
        Returns:
            datetime: The parsed datetime object.
        """
        # Try multiple formats if needed
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Invalid timestamp format: {value}")
