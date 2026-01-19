import psycopg2

# Connection parameters
DB_HOST = "localhost"        # PostgreSQL is running locally
DB_NAME = "energy_db"        # The database you created in psql
DB_USER = "postgres"         # The superuser you set up
DB_PASS = "YourPasswordHere" # Replace with the password you chose during initdb

def ingest_logs_from_file(file_path):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        print("✅ Connected to PostgreSQL successfully!")

        # Open and read sensor_logs.txt
        with open(file_path, "r") as f:
            for line in f:
                # Skip empty lines
                if not line.strip():
                    continue

                # Split by comma
                timestamp, temp, hum, irr, wind = line.strip().split(",")

                # Insert into table
                cur.execute("""
                    INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
                    VALUES (%s, %s, %s, %s, %s);
                """, (timestamp, float(temp), float(hum), float(irr), float(wind)))

        conn.commit()
        print("✅ Logs ingested successfully!")

        # Verify by fetching last 5 rows
        cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 5;")
        rows = cur.fetchall()
        print("📊 Latest sensor_data rows:")
        for row in rows:
            # row[1] is the timestamp column
            ts = row[1].strftime("%Y-%m-%d %H:%M:%S")  # format without microseconds
            print((row[0], ts, row[2], row[3], row[4], row[5]))

        cur.close()
        conn.close()        

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    ingest_logs_from_file("sensor_logs.txt")
