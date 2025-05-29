# EcoWatch Environmental Monitoring System

EcoWatch is a modular and extensible Python application for processing, validating, and reporting environmental sensor data. It is designed to help organizations monitor environmental conditions in real time, detect anomalies, and generate executive reports for decision-making.

## Features
- **Log ingestion and validation** from CSV (easily extensible to other formats)
- **In-memory cache** for fast access to the latest 5 minutes of data
- **Object-oriented design** for maintainability and scalability
- **Executive reports** using Factory and Strategy design patterns
- **Easily extensible** to new report types, data sources, and business rules
- **Tabular report output** using pandas

## System Architecture Diagram

```
+-------------------+
|   CSV Log File    |
+-------------------+
           |
           v
+-------------------+
|    LogReader      |  -- Reads & validates logs
+-------------------+
           |
           v
+-------------------+
|  TemporalCache    |  -- (Optional) Keeps last 5 min logs
+-------------------+
           |
           v
+-------------------+
|  ReportFactory    |  -- Instantiates report objects
+-------------------+
           |
   +-------+-------+
   |               |
   v               v
+-------------------+    +-------------------+
| StateByRoomReport |    | CriticalAlertsRep.|
+-------------------+    +-------------------+
   |                       |
   v                       v
+-------------------+    +-------------------+
| StateByRoomStrat. |    | CriticalAlertsStr.|
+-------------------+    +-------------------+
   |                       |
   v                       v
+-------------------+    +-------------------+
|  DataFrame Output |    |  DataFrame Output |
+-------------------+    +-------------------+
```

**Legend:**
- `LogReader`: Reads and validates logs from CSV.
- `TemporalCache`: (Optional, for real-time queries) Keeps the last 5 minutes of logs in memory.
- `ReportFactory`: Instantiates report objects.
- `StateByRoomReport` / `CriticalAlertsReport`: Report types using the Strategy pattern.
- `DataFrame Output`: Tabular report for executive use.

## Project Structure
```
homework-entregable/
├── dataset/
│   └── logs_ambientales_ecowatch.csv
├── src/
│   ├── __main__.py
│   ├── log.py
│   ├── sala.py
│   ├── cache.py
│   ├── log_reader.py
│   ├── report.py
│   ├── report_factory.py
│   ├── report_strategy.py
│   ├── reports_state_by_room.py
│   └── reports_critical_alerts.py
├── requirements.txt
├── README.md
└── EXPLAINME.md
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd homework-entregable
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main script with your log file:
```bash
python -m src dataset/logs_ambientales_ecowatch.csv
```
This will print two reports to the console:
- **State by Room Report:** Average temperature, humidity, CO₂, and most common state per room.
- **Critical Alerts Report:** All logs where temperature, humidity, or CO₂ exceed critical thresholds.

## How It Works
- **LogReader** reads and validates logs from CSV.
- **TemporalCache** (see `src/cache.py`) keeps only the last 5 minutes of logs in memory.
- **ReportFactory** creates report objects based on type.
- **Strategy pattern** allows each report to have its own logic.
- **Reports are easily extensible:** You can add a new report type by creating a new report and strategy class, then registering it in the factory—**without modifying or rewriting existing code**. This is possible thanks to the Factory and Strategy design patterns.

## Extending the System
- **Add new log sources** (e.g., JSON) by extending `LogReader`.
- **Add new reports** by creating a new report and strategy class, then register it in `ReportFactory`. **No changes to existing code are needed.**
- **Adjust thresholds or business rules** in the strategy classes.

### Example: Adding a New Report
1. Create a new strategy class (e.g., `MyNewReportStrategy`) implementing the logic you need.
2. Create a new report class (e.g., `MyNewReport`) that uses your strategy.
3. Register your new report in the factory:
   ```python
   factory.register_report("my_new_report", MyNewReport)
   ```
4. Now you can create and use your new report type without touching or rewriting any existing report code.

## Requirements
- Python 3.7+
- pandas

## License
MIT (or specify your license)

## Author
Diego Feresin

## Design Decisions and Rationale

As a technical professional, it is essential to communicate the reasoning behind each design choice. This section explains and justifies the main decisions made during the development of EcoWatch, so that other teams can understand, maintain, and scale the system in the future.

### Data Structures
- **Deque for Temporal Cache:**
  - Chosen for its O(1) append and pop operations at both ends, making it ideal for a sliding time window of logs.
  - **Alternative:** A list or set would require O(n) operations for purging old logs, reducing efficiency.
- **Pandas DataFrame for Log Processing and Reporting:**
  - Enables efficient tabular data manipulation, aggregation, and validation.
  - **Alternative:** Manual iteration and aggregation would be more verbose, error-prone, and less performant.

### Validation Approach
- **Centralized Validation in LogReader:**
  - All log validation is handled in one place, making it easy to update rules and ensure data quality.
  - **Alternative:** Scattered validation logic would make maintenance harder and increase the risk of inconsistent checks.

### Design Patterns
- **Factory Pattern:**
  - Used in `ReportFactory` to decouple report creation from usage, allowing new report types to be added without modifying existing code.
  - **Alternative:** Hardcoding report instantiation would make the system rigid and harder to extend.
- **Strategy Pattern:**
  - Each report delegates its logic to a strategy class, making it easy to add new processing logic or change existing logic without affecting other parts of the system.
  - **Alternative:** Embedding all logic in the report classes would violate the open/closed principle and hinder extensibility.

### Optimization Techniques
- **In-memory cache for recent logs:**
  - Ensures real-time access to the latest data, critical for operational decisions.
  - **Alternative:** Querying a database for every request would introduce unnecessary latency for recent data.
- **Efficient purging and filtering:**
  - The cache purges old logs based on timestamps, not arrival order, ensuring correct handling of late or out-of-order events.

### Simplicity, Efficiency, and Extensibility
- **Simplicity:**
  - The codebase is organized by responsibility, with clear separation between log ingestion, caching, and reporting.
- **Efficiency:**
  - Chosen data structures and libraries (deque, pandas) are optimized for the problem domain.
- **Extensibility:**
  - New log sources, reports, or business rules can be added with minimal changes, thanks to OOP and design patterns.

### Summary
Every key decision was made to balance clarity, performance, and future growth. The architecture is modular, maintainable, and ready for new requirements, ensuring that EcoWatch can evolve as monitoring needs change.

## Running the API (FastAPI)

To run the EcoWatch API developed with FastAPI:

### 1. Install FastAPI and Uvicorn (if you haven't already):
```bash
pip install fastapi uvicorn
```

### 2. Run the server with Uvicorn
From the project root, run:
```bash
uvicorn src.api:app --reload
```
- `src.api:app` means the `app` object is in the file `src/api.py`.
- `--reload` enables auto-reload on code changes (useful for development).

### 3. Access the API
- **Interactive docs:**  [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc docs:**  [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Example available endpoints
- `GET /logs`  — Returns validated logs (you can limit the amount with the `limit` parameter).
- `GET /report/state_by_room`  — Returns the state by room report.
- `GET /report/critical_alerts`  — Returns the critical alerts report.

### 5. Exporting Reports as CSV or XLSX
- `GET /report/state_by_room/export?format=csv|xlsx` — Download the state by room report as CSV or XLSX.
- `GET /report/critical_alerts/export?format=csv|xlsx` — Download the critical alerts report as CSV or XLSX.

Example URLs:
- Download state by room as CSV: `http://localhost:8000/report/state_by_room/export?format=csv`
- Download critical alerts as XLSX: `http://localhost:8000/report/critical_alerts/export?format=xlsx`

Example cURL requests:
```bash
curl -o state_by_room_report.csv "http://localhost:8000/report/state_by_room/export?format=csv"
curl -o state_by_room_report.xlsx "http://localhost:8000/report/state_by_room/export?format=xlsx"
curl -o critical_alerts_report.csv "http://localhost:8000/report/critical_alerts/export?format=csv"
curl -o critical_alerts_report.xlsx "http://localhost:8000/report/critical_alerts/export?format=xlsx"
```

### 6. Query Logs by Date Range, Room, and Sensor
- `GET /logs/query?start_time_date=YYYY-MM-DD HH:MM:SS&end_time_date=YYYY-MM-DD HH:MM:SS&room=RoomName[&sensor=SensorName]` — Returns logs filtered by date range, room, and optionally sensor.

Example URL:
- `http://localhost:8000/logs/query?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room1`

Example cURL requests:
```bash
curl "http://localhost:8000/logs/query?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room1"
curl "http://localhost:8000/logs/query?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room2&sensor=SensorA"
```

#### Exporting Query Results
- `GET /logs/query/export?start_time_date=...&end_time_date=...&room=...&sensor=...&format=csv|xlsx` — Download the filtered logs as CSV or XLSX.

Example:
```bash
curl -o filtered_logs.csv "http://localhost:8000/logs/query/export?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room1&format=csv"
curl -o filtered_logs.xlsx "http://localhost:8000/logs/query/export?start_time_date=2024-06-01%2012:00:00&end_time_date=2024-06-01%2013:00:00&room=Room2&sensor=SensorA&format=xlsx"
```

For extra info about decision making for this project, please read the [EXPLAINME.md](EXPLAINME.md) file.
