import streamlit as st
import psycopg2
import pandas as pd

# ----------------------------
# Connect to PostgreSQL
# ----------------------------
conn = psycopg2.connect(
    dbname="energy_db",
    user="postgres",
    password="PdM",   # <-- replace with your DB password
    host="localhost",
    port="5432"
)

# ----------------------------
# Load data into Pandas
# ----------------------------
df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 200;", conn)

# ----------------------------
# Streamlit Dashboard
# ----------------------------
st.title("Energy Sensor Dashboard")

st.write("Latest sensor readings from database:")

# Show table
st.dataframe(df)

# Line charts
st.subheader("Temperature Trend")
st.line_chart(df.set_index("timestamp")[["temperature"]])

st.subheader("Humidity Trend")
st.line_chart(df.set_index("timestamp")[["humidity"]])

st.subheader("Irradiance Trend")
st.line_chart(df.set_index("timestamp")[["irradiance"]])

st.subheader("Wind Speed Trend")
st.line_chart(df.set_index("timestamp")[["wind_speed"]])

conn.close()
