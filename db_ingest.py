import psycopg2
from tabulate import tabulate
from api_wrappers.openweather import get_weather_data

DB_HOST = "localhost"
DB_NAME = "energy_db"
DB_USER = "postgres"
DB_PASS = "PdM"   # <-- SQL password

def save_to_log(file_path, row):
    """Append sensor data to sensor_log.txt"""
    with open(file_path, "a") as f:
        f.write(",".join(map(str, row)) + "\n")

def ingest_to_db(row):
    """Insert sensor data into PostgreSQL"""
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()

    # Insert into sensor_data table
    cur.execute("""
        INSERT INTO sensor_data (timestamp, wind_speed, humidity, irradiance, temperature)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (timestamp) DO NOTHING;
    """, (row[0], row[1], row[2], row[3], 0))  # temperature dummy for now

    conn.commit()
    cur.close()
    conn.close()

def export_to_html(file_path="sensor_output.html"):
    """Export latest 50 rows to HTML"""
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 50;")
    rows = cur.fetchall()

    formatted_rows = []
    for r in rows:
        ts = r[1].strftime("%Y-%m-%d %H:%M:%S")  # no microseconds
        formatted_rows.append((r[0], ts, r[2], r[3], r[4], r[5]))

    html = f"""
    <html>
    <head>
        <title>Sensor Data Output</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
            th {{ background-color: #f4f4f4; }}
        </style>
    </head>
    <body>
        <h2>Latest 50 Sensor Data Rows (Wind & Solar)</h2>
        {tabulate(formatted_rows, headers=["ID","Timestamp","Temp","Humidity","Irradiance","Wind"], tablefmt="html")}
    </body>
    </html>
    """

    with open(file_path, "w") as f:
        f.write(html)

    cur.close()
    conn.close()
    print(f"✅ HTML output written to {file_path}")

if __name__ == "__main__":
    new_row = get_weather_data()
    save_to_log("sensor_log.txt", new_row)
    ingest_to_db(new_row)
    export_to_html("sensor_output.html")
