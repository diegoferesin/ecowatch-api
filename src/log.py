class Log:
    """
    Represents an environmental log entry from a sensor.
    Each log contains a timestamp, room (sala), state, temperature, humidity, CO2 level, and an optional message.
    """
    def __init__(self, timestamp, sala, estado, temperatura, humedad, co2, mensaje=None):
        """
        Initialize a Log instance.

        Args:
            timestamp (datetime): The timestamp of the log entry.
            sala (str): The room or area being monitored.
            estado (str): The state or status of the room/sensor.
            temperatura (float): The temperature value.
            humedad (float): The humidity value.
            co2 (float): The CO2 level.
            mensaje (str, optional): An optional message or alert.
        """
        self.timestamp = timestamp
        self.sala = sala
        self.estado = estado
        self.temperatura = temperatura
        self.humedad = humedad
        self.co2 = co2
        self.mensaje = mensaje
