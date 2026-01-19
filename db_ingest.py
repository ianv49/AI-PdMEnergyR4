import psycopg2
import requests

# Connection parameters
DB_HOST = "localhost"        # PostgreSQL is running locally
DB_NAME = "energy_db"        # The database you created in psql
DB_USER = "postgres"         # The superuser you set up
DB_PASS = "PdM"              # <-- Your PostgreSQL password

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
