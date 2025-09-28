import streamlit as st
import pandas as pd
import time
from generator import generate_log

# Buffers to store logs + alerts
logs = []
alerts = []

# Streamlit page setup
st.set_page_config("Log Anomaly Detector", layout="wide")
st.title("🚨 Log Anomaly Detector")

# Alert box at top
alert_box = st.empty()

# Split into two columns for chart + table
col1, col2 = st.columns(2)

# --- Create chart once ---
chart = col1.line_chart([])   # left column for chart
log_table = col2.empty()      # right column for table

# Insights section (below chart + table)
st.markdown("### 📊 Log Insights")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
avg_placeholder = metric_col1.empty()
p95_placeholder = metric_col2.empty()
error_placeholder = metric_col3.empty()
anomaly_placeholder = metric_col4.empty()

# Main loop simulates log stream
while True:
    # Generate log (generator decides if anomaly or not)
    log = generate_log()

    # Check anomaly flag directly
    if log.get("anomaly", False):
        alerts.append(log)

    # Add to logs
    logs.append(log)

    # Convert last N logs into a DataFrame (for display)
    df = pd.DataFrame(logs[-5000:])

    # --- Update chart data (no flashing) ---
    if not df.empty and "latency_ms" in df.columns:
        chart.add_rows(df[["latency_ms"]].tail(1))  # append new point only

    # Update log table in right column
    log_table.dataframe(df.tail(20))  # show last 20 logs

    # Show alerts if anomalies found
    if alerts:
        alert_box.error(f"⚠️ Anomalies detected: {len(alerts)}")

    # --- Insights panel calculations ---
    if not df.empty:
        avg_latency = df["latency_ms"].mean()
        p95_latency = df["latency_ms"].quantile(0.95)
        error_rate = (df["level"] == "ERROR").mean() * 100 if "level" in df.columns else 0


        avg_placeholder.metric("Avg Latency (ms)", f"{avg_latency:.1f}")
        p95_placeholder.metric("95th Percentile Latency", f"{p95_latency:.1f}")
        error_placeholder.metric("Error Rate", f"{error_rate:.1f}%")


    # Small pause to simulate stream
    time.sleep(0.1)
