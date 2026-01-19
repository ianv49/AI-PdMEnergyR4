import psycopg2
from datetime import datetime

# Connection parameters
DB_HOST = "localhost"        # PostgreSQL is running locally
DB_NAME = "energy_db"        # The database you created in psql
DB_USER = "postgres"         # The superuser you set up
DB_PASS = "onsemi111!" # Replace with the password you chose during initdb

def ingest_log():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Connected to PostgreSQL successfully!")

        # Create a cursor to run SQL commands
        cur = conn.cursor()

        # Example: insert one test row
        cur.execute("""
            INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
            VALUES (%s, %s, %s, %s, %s);
        """, (datetime.now(), 28.5, 65.2, 450.0, 5.8))

        # Commit changes
        conn.commit()
        print("✅ Test row inserted!")

        # Fetch last 5 rows
        cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 5;")
        rows = cur.fetchall()
        print("📊 Latest sensor_data rows:")
        for row in rows:
            print(row)

        # Close connection
        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error connecting to PostgreSQL:", e)

if __name__ == "__main__":
    ingest_log()
