from collections import deque
from datetime import datetime, timedelta

class TemporalCache:
    """
    In-memory cache to store environmental logs for the last 5 minutes.
    Allows fast queries by room or timestamp.
    Handles late events and ensures only relevant logs are kept.
    """
    def __init__(self, window_minutes=5):
        """
        Initialize the temporal cache.

        Args:
            window_minutes (int): The time window in minutes to keep logs in cache.
        """
        self.window = timedelta(minutes=window_minutes)
        self.logs = deque()

    def add_log(self, log):
        """
        Add a log to the cache and remove outdated logs.

        Args:
            log (Log): The log entry to add.
        """
        self.logs.append(log)
        self._purge_old_logs()

    def _purge_old_logs(self):
        """
        Remove logs that are outside the time window from the cache.
        """
        now = datetime.now()
        while self.logs and (now - self.logs[0].timestamp) > self.window:
            self.logs.popleft()

    def get_logs_by_room(self, room):
        """
        Retrieve all logs for a specific room within the time window.

        Args:
            room (str): The room name to filter logs.
        Returns:
            list: List of Log objects for the specified room.
        """
        return [log for log in self.logs if log.sala == room]

    def get_logs_by_timestamp(self, timestamp):
        """
        Retrieve all logs for a specific timestamp within the time window.

        Args:
            timestamp (datetime): The timestamp to filter logs.
        Returns:
            list: List of Log objects for the specified timestamp.
        """
        return [log for log in self.logs if log.timestamp == timestamp]
