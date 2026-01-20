from db_connector import get_connection

def main():
    # Try to connect
    conn = get_connection()

    # If connection works, print success message
    print("✅ Database connection test successful!")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
