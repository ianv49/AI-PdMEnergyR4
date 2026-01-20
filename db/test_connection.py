from db_connector import get_connection

def main():
    # Step 1: Try to connect
    conn = get_connection()

    # Step 2: Run a simple query
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM sensor_data;")
            result = cur.fetchone()
            print(f"✅ Database connection test successful!")
            print(f"📊 sensor_data table has {result[0]} rows.")
    except Exception as e:
        print(f"❌ Query failed: {e}")

    # Step 3: Close connection
    conn.close()

if __name__ == "__main__":
    main()
