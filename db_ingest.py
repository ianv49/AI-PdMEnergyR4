import psycopg2   # PostgreSQL connector

# --- Database connection settings ---
# Replace these with your actual PostgreSQL setup
DB_HOST = "localhost"          # usually localhost if running locally
DB_NAME = "your_database_name" # the database you created in PostgreSQL
DB_USER = "your_username"      # your PostgreSQL username
DB_PASS = "your_password"      # your PostgreSQL password

def ingest_logs():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # Open the sensor log file
    with open("sensor_logs.txt", "r") as f:
        for line in f:
            # Each line looks like:
            # 2026-01-19 18:53:17, 31.0, 54.12, 655.98, 11.03
            parts = line.strip().split(", ")
            if len(parts) == 5:
                timestamp, temp, hum, irr, wind = parts

                # Insert into the database
                cur.execute(
                    """
                    INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (timestamp, float(temp), float(hum), float(irr), float(wind))
                )

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    print("Logs ingested successfully!")

if __name__ == "__main__":
    ingest_logs()
