from db_connector import get_connection

def main():
    # Step 1: Connect to DB
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            # Step 2: Count rows
            cur.execute("SELECT COUNT(*) FROM sensor_data;")
            result = cur.fetchone()
            print("✅ Database connection test successful!")
            print(f"📊 sensor_data table has {result[0]} rows.")

            # Step 3: Show top 2 rows (earliest timestamps)
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp ASC LIMIT 2;")
            top_rows = cur.fetchall()
            print("\n🔎 Top 2 rows (earliest):")
            for row in top_rows:
                print(row)

            # Step 4: Show bottom 2 rows (latest timestamps)
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 2;")
            bottom_rows = cur.fetchall()
            print("\n🔎 Bottom 2 rows (latest):")
            for row in bottom_rows:
                print(row)

    except Exception as e:
        print(f"❌ Query failed: {e}")

    # Step 5: Close connection
    conn.close()

if __name__ == "__main__":
    main()
