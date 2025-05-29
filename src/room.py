class Room:
    """
    Represents a monitored room or area in the EcoWatch system.
    Each Room can have multiple logs and is identified by its name.
    """
    def __init__(self, name):
        """
        Initialize a Room instance.

        Args:
            name (str): The name or identifier of the room.
        """
        self.name = name
        self.logs = []

    def add_log(self, log):
        """
        Add a log entry to the room.

        Args:
            log (Log): The log entry to add.
        """
        self.logs.append(log)
