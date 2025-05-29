from src.log_reader import LogReader
from src.report_factory import ReportFactory
import sys

if __name__ == "__main__":
    """
    Example main script for EcoWatch log processing and reporting.
    Reads logs from a CSV file, generates reports using the factory, and prints the results.
    """
    # You can pass the CSV file path as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python -m src <path_to_logs.csv>")
        sys.exit(1)
    log_path = sys.argv[1]

    # Read and validate logs
    reader = LogReader(log_path)
    logs = reader.read_logs()
    print(f"Loaded {len(logs)} valid logs.")

    # Set up the report factory and register default reports
    factory = ReportFactory()
    factory.register_default_reports()

    # Generate and print State by Room report
    state_report = factory.create_report("state_by_room")
    state_df = state_report.generate(logs)
    print("\nState by Room Report:")
    print(state_df)

    # Generate and print Critical Alerts report
    alerts_report = factory.create_report("critical_alerts")
    alerts_df = alerts_report.generate(logs)
    print("\nCritical Alerts Report:")
    print(alerts_df) 