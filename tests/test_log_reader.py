import pytest
import pandas as pd
from src.log_reader import LogReader
from src.log import Log
import tempfile

# Helper to create a temporary CSV file
def create_temp_csv(content):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w')
    tmp.write(content)
    tmp.close()
    return tmp.name

def test_read_valid_logs():
    csv_content = """timestamp,sala,estado,temperatura,humedad,co2,mensaje
2024-06-01 12:00:00,Room1,OK,22.5,45.0,400,All good
2024-06-01 12:01:00,Room2,OK,23.0,50.0,420,All good
"""
    path = create_temp_csv(csv_content)
    reader = LogReader(path)
    logs = reader.read_logs()
    assert len(logs) == 2
    assert all(isinstance(log, Log) for log in logs)

def test_read_invalid_logs():
    csv_content = """timestamp,sala,estado,temperatura,humedad,co2,mensaje
2024-06-01 12:00:00,Room1,OK,22.5,45.0,,All good
,Room2,OK,23.0,50.0,420,All good
"""
    path = create_temp_csv(csv_content)
    reader = LogReader(path)
    logs = reader.read_logs()
    # Both rows are invalid: one missing co2, one missing timestamp
    assert len(logs) == 0
