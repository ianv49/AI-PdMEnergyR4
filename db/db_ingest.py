import logging
import csv
from datetime import datetime
from tabulate import tabulate
from db_connector import get_connection   # Import connection function
import logging
import os

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Create handlers (use logging, not logger)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs/ingestion.log", mode="a")

# Set formatter
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Create logger object
logger = logging.getLogger("ingestion_logger")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers if script is re-run
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Logging setup: console + file
logger.basicConfig(
    level=logger.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logger.StreamHandler(),                        # print to console
        logger.FileHandler("logs/ingestion.log", mode="a")  # save to file
    ]
)

def count_rows(conn):
    """Return the number of rows in sensor_data table."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM sensor_data;")
            result = cur.fetchone()
            return result[0]
    except Exception as e:
        logger.error(f"Error counting rows: {e}")
        return None

def insert_sensor_data(conn, timestamp, temperature, humidity, irradiance, wind_speed):
    """Insert one row into sensor_data table, strip microseconds, skip duplicates."""
    try:
        ts = datetime.fromisoformat(timestamp).replace(microsecond=0)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (timestamp) DO NOTHING;
                """,
                (ts, temperature, humidity, irradiance, wind_speed)
            )
        conn.commit()
    except Exception as e:
        logger.error(f"Insert failed: {e}")

def ingest_text_file(conn, filepath="data/sensor_logs.txt"):
    """Read plain text log file and insert rows."""
    try:
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                # Skip header line
                if parts[0].lower() == "timestamp":
                    continue
                if len(parts) == 5:
                    timestamp, temperature, humidity, irradiance, wind_speed = parts
                    insert_sensor_data(conn, timestamp, float(temperature), float(humidity), float(irradiance), float(wind_speed))
        logger.info("Text file ingestion complete.")
    except FileNotFoundError:
        logger.warning(f"{filepath} not found.")
    except Exception as e:
        logger.error(f"Error ingesting text file: {e}")


def ingest_csv_file(conn, filepath="data/sensor_data.csv"):
    """Read CSV file and insert rows."""
    try:
        with open(filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                insert_sensor_data(
                    conn,
                    row["timestamp"],
                    float(row["temperature"]),
                    float(row["humidity"]),
                    float(row["irradiance"]),
                    float(row["wind_speed"])
                )
        logger.info("CSV ingestion complete.")
    except FileNotFoundError:
        logger.warning(f"{filepath} not found.")
    except Exception as e:
        logger.error(f"Error ingesting CSV file: {e}")

def fetch_and_display(conn, limit=10):
    """Display latest rows in a pretty table."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT %s;", (limit,))
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            print(tabulate(rows, headers=headers, tablefmt="psql"))
    except Exception as e:
        logger.error(f"Error fetching rows: {e}")

if __name__ == "__main__":
    conn = get_connection()

    # Step 1: Count rows before ingestion
    before_count = count_rows(conn)
    print(f"📊 Rows before ingestion: {before_count}")

    # Step 2: Run ingestion
    ingest_text_file(conn, "data/sensor_logs.txt")
    ingest_csv_file(conn, "data/sensor_data.csv")

    # Step 3: Count rows after ingestion
    after_count = count_rows(conn)
    print(f"📊 Rows after ingestion: {after_count}")

    # Step 4: Show how many new rows were added
    if before_count is not None and after_count is not None:
        print(f"✅ New rows added: {after_count - before_count}")

    # Step 5: Display latest rows
    fetch_and_display(conn, limit=10)

    conn.close()
