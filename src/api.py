from fastapi import FastAPI, Query
from src.log_reader import LogReader
from src.report_factory import ReportFactory
import pandas as pd
import os
from dotenv import load_dotenv

app = FastAPI(title="EcoWatch API")

# Load environment variables from .env
load_dotenv()
LOGS_PATH = os.getenv("LOGS_PATH", "dataset/logs_ambientales_ecowatch.csv")

# Load logs and set up factory at startup (for demo purposes)
log_reader = LogReader(LOGS_PATH)
logs = log_reader.read_logs()
report_factory = ReportFactory()
report_factory.register_default_reports()

@app.get("/logs")
def get_logs(limit: int = Query(100, ge=1, le=1000)):
    """
    Get a list of validated logs (limited).
    """
    return [log.__dict__ for log in logs[:limit]]

@app.get("/report/state_by_room")
def get_state_by_room():
    """
    Get the state by room report as JSON.
    """
    report = report_factory.create_report("state_by_room")
    df = report.generate(logs)
    return df.to_dict(orient="records")

@app.get("/report/critical_alerts")
def get_critical_alerts():
    """
    Get the critical alerts report as JSON.
    """
    report = report_factory.create_report("critical_alerts")
    df = report.generate(logs)
    return df.to_dict(orient="records") 