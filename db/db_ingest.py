import os
import sys
import psycopg2
import logging
import csv

#Update db_ingest.py to load .env:
from dotenv import load_dotenv
load_dotenv()

from tabulate import tabulate

# ----------------------------
# Logging Setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ----------------------------
# Database Connection
# ----------------------------
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "energy_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "PdM"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        logging.info("Connected to PostgreSQL successfully.")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        sys.exit(1)

# ----------------------------
# Insert Function with Duplicate Handling
# ----------------------------
from datetime import datetime
def insert_sensor_data(conn, timestamp, temperature, humidity, irradiance, wind_speed):
    try:
        # Parse and reformat timestamp to seconds only
        ts = datetime.fromisoformat(timestamp)
        ts = ts.replace(microsecond=0)

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
        logging.error(f"Insert failed: {e}")

# ----------------------------
# Ingest from Plain Text Logs
# ----------------------------
def ingest_text_file(conn, filepath="sensor_logs.txt"):
    try:
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    timestamp, sensor_id, value = parts
                    insert_sensor_data(conn, timestamp, sensor_id, float(value))
        logging.info("Text file ingestion complete.")
    except FileNotFoundError:
        logging.warning(f"{filepath} not found.")
    except Exception as e:
        logging.error(f"Error ingesting text file: {e}")

# ----------------------------
# Ingest from CSV
# ----------------------------
def ingest_csv_file(conn, filepath="data/sensor_data.csv"):
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
        logging.info("CSV ingestion complete.")
    except FileNotFoundError:
        logging.warning(f"{filepath} not found.")
    except Exception as e:
        logging.error(f"Error ingesting CSV file: {e}")

# ----------------------------
# Display Latest Rows
# ----------------------------
def fetch_and_display(conn, limit=10):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT %s;", (limit,))
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            print(tabulate(rows, headers=headers, tablefmt="psql"))
    except Exception as e:
        logging.error(f"Error fetching rows: {e}")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    conn = get_connection()
    ingest_text_file(conn, "data/sensor_logs.txt")
    ingest_csv_file(conn, "data/sensor_data.csv")   # optional CSV ingestion
    
    fetch_and_display(conn, limit=10)
    conn.close()
