from fastapi import FastAPI, Query, Response
from fastapi.responses import StreamingResponse
from typing import Optional
from src.log_reader import LogReader
from src.report_factory import ReportFactory, export_report
import pandas as pd
import os
from dotenv import load_dotenv
import io
from datetime import datetime

app = FastAPI(title="EcoWatch API")

# Load environment variables from .env
load_dotenv()
LOGS_PATH = os.getenv("LOGS_PATH", "dataset/logs_ambientales_ecowatch.csv")

# Load logs and set up factory at startup (for demo purposes)
log_reader = LogReader(LOGS_PATH)
logs = log_reader.read_logs()
report_factory = ReportFactory()
report_factory.register_default_reports()

EXPORT_DIRS = {
    "csv": "src/reports/csv",
    "xlsx": "src/reports/xlsx"
}

@app.get("/logs")
def get_logs(limit: int = Query(100, ge=1, le=1000)):
    """
    Get a list of validated logs (limited).
    """
    return [log.__dict__ for log in logs[:limit]]

@app.get("/logs/query")
def query_logs(
    start_time_date: str = Query(..., description="Start datetime in YYYY-MM-DD HH:MM:SS format"),
    end_time_date: str = Query(..., description="End datetime in YYYY-MM-DD HH:MM:SS format"),
    room: str = Query(..., description="Room name to filter logs"),
    sensor: Optional[str] = Query(None, description="Sensor name to filter logs (optional)")
):
    """
    Query logs by date range, room, and optionally sensor.
    """
    try:
        start_dt = datetime.strptime(start_time_date, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_time_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}
    filtered = []
    for log in logs:
        if not (start_dt <= log.timestamp <= end_dt):
            continue
        if log.sala != room:
            continue
        # If sensor field exists in log, filter by it
        if sensor is not None and hasattr(log, 'sensor') and getattr(log, 'sensor', None) != sensor:
            continue
        filtered.append(log.__dict__)
    return filtered

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

@app.get("/report/state_by_room/export")
def export_state_by_room(format: str = Query("csv", enum=["csv", "xlsx"])):
    """
    Export the state by room report as CSV or XLSX, save it to disk, and return it.
    """
    report = report_factory.create_report("state_by_room")
    df = report.generate(logs)
    buf = io.BytesIO()
    export_dir = EXPORT_DIRS[format]
    os.makedirs(export_dir, exist_ok=True)
    if format == "csv":
        filename = os.path.join(export_dir, "state_by_room_report.csv")
        df.to_csv(filename, index=False)
        df.to_csv(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=state_by_room_report.csv"})
    elif format == "xlsx":
        filename = os.path.join(export_dir, "state_by_room_report.xlsx")
        df.to_excel(filename, index=False)
        df.to_excel(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=state_by_room_report.xlsx"})

@app.get("/report/critical_alerts/export")
def export_critical_alerts(format: str = Query("csv", enum=["csv", "xlsx"])):
    """
    Export the critical alerts report as CSV or XLSX, save it to disk, and return it.
    """
    report = report_factory.create_report("critical_alerts")
    df = report.generate(logs)
    buf = io.BytesIO()
    export_dir = EXPORT_DIRS[format]
    os.makedirs(export_dir, exist_ok=True)
    if format == "csv":
        filename = os.path.join(export_dir, "critical_alerts_report.csv")
        df.to_csv(filename, index=False)
        df.to_csv(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=critical_alerts_report.csv"})
    elif format == "xlsx":
        filename = os.path.join(export_dir, "critical_alerts_report.xlsx")
        df.to_excel(filename, index=False)
        df.to_excel(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=critical_alerts_report.xlsx"})

@app.get("/logs/query/export")
def export_query_logs(
    start_time_date: str = Query(..., description="Start datetime in YYYY-MM-DD HH:MM:SS format"),
    end_time_date: str = Query(..., description="End datetime in YYYY-MM-DD HH:MM:SS format"),
    room: str = Query(..., description="Room name to filter logs"),
    sensor: Optional[str] = Query(None, description="Sensor name to filter logs (optional)"),
    format: str = Query("csv", enum=["csv", "xlsx"])
):
    """
    Export filtered logs by date range, room, and optionally sensor as CSV or XLSX.
    """
    try:
        start_dt = datetime.strptime(start_time_date, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_time_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}
    filtered = []
    for log in logs:
        if not (start_dt <= log.timestamp <= end_dt):
            continue
        if log.sala != room:
            continue
        if sensor is not None and hasattr(log, 'sensor') and getattr(log, 'sensor', None) != sensor:
            continue
        filtered.append(log.__dict__)
    df = pd.DataFrame(filtered)
    buf = io.BytesIO()
    export_dir = EXPORT_DIRS[format]
    os.makedirs(export_dir, exist_ok=True)
    if format == "csv":
        filename = os.path.join(export_dir, "filtered_logs.csv")
        df.to_csv(filename, index=False)
        df.to_csv(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=filtered_logs.csv"})
    elif format == "xlsx":
        filename = os.path.join(export_dir, "filtered_logs.xlsx")
        df.to_excel(filename, index=False)
        df.to_excel(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=filtered_logs.xlsx"}) 