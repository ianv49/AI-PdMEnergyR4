import psycopg2
import requests
from tabulate import tabulate   # <-- new import

# Connection parameters
DB_HOST = "localhost"        
DB_NAME = "energy_db"        
DB_USER = "postgres"         
DB_PASS = "PdM"               # <-- your PostgreSQL password

# Example sensor API endpoint (replace with your real sensor URL)
SENSOR_API = "http://example.com/api/sensor"

def fetch_sensor_data():
    """Fetch new data from web sensor API."""
    response = requests.get(SENSOR_API)
    data = response.json()
    return (
        data["timestamp"],
        float(data["temperature"]),
        float(data["humidity"]),
        float(data["irradiance"]),
        float(data["wind_speed"])
    )

def save_to_log(file_path, row):
    """Append sensor data to sensor_logs.txt."""
    with open(file_path, "a") as f:
        f.write(",".join(map(str, row)) + "\n")

def ingest_to_db(row):
    """Insert sensor data into PostgreSQL with duplicate protection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING;
        """, row)

        conn.commit()

        # Fetch last 5 rows for display
        cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 5;")
        rows = cur.fetchall()

        # Format timestamp without microseconds
        formatted_rows = []
        for r in rows:
            ts = r[1].strftime("%Y-%m-%d %H:%M:%S")
            formatted_rows.append((r[0], ts, r[2], r[3], r[4], r[5]))

        print("📊 Latest sensor_data rows:")
        print(tabulate(formatted_rows, headers=["ID","Timestamp","Temp","Humidity","Irradiance","Wind"], tablefmt="psql"))

        cur.close()
        conn.close()
        print("✅ Data ingested into database:", row)

    except Exception as e:
        print("❌ Error inserting into database:", e)

if __name__ == "__main__":
    # Step 1: Fetch new data from web sensor
    new_row = fetch_sensor_data()

    # Step 2: Save to sensor_logs.txt
    save_to_log("sensor_logs.txt", new_row)
    print("✅ Data appended to sensor_logs.txt")

    # Step 3: Insert into PostgreSQL
    ingest_to_db(new_row)
