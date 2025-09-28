import streamlit as st
import pandas as pd
import time
from detector import AnomalyDetector
from generator import generate_log

# Create detector instance
detector = AnomalyDetector()

# Buffers to store logs + alerts
logs = []
alerts = []

# Streamlit page setup
st.set_page_config("Log Anomaly Detector", layout="wide")
st.title("Log Anomaly Detector")

# Alert box at top
alert_box = st.empty()

# Split into two columns
col1, col2 = st.columns(2)
chart_placeholder = col1.empty()   # left column for chart
log_table = col2.empty()           # right column for table

# Main loop simulates log stream
while True:
    # Check if we’re in anomaly window (every 30s for 5s)
    elapsed = int(time.time()) % 30 < 5
    log = generate_log(is_anomaly=elapsed)

    # Check anomaly using detector
    if detector.check(log):
        alerts.append(log)

    # Add to logs
    logs.append(log)

    # Convert last 50 logs into a DataFrame (for display)
    df = pd.DataFrame(logs[-5000:])

    # Update chart in left column
    if not df.empty and "latency_ms" in df.columns:
        chart_placeholder.line_chart(df["latency_ms"])

    # Update log table in right column
    log_table.dataframe(df)

    # Show alerts if anomalies found
    if alerts:
        alert_box.error(f"Anomalies detected: {len(alerts)}")

    # Small pause to simulate stream
    time.sleep(0.5)
