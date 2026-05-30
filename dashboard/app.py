import requests
import streamlit as st

st.set_page_config(
    page_title="Store Intelligence",
    layout="wide"
)

STORE_ID = "STORE_BLR_002"

metrics = requests.get(
    f"http://localhost:8000/stores/{STORE_ID}/metrics"
).json()

anomalies = requests.get(
    f"http://localhost:8000/stores/{STORE_ID}/anomalies"
).json()

st.title("🏪 Store Intelligence Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Visitors",
    metrics["unique_visitors"]
)

c2.metric(
    "Conversion %",
    metrics["conversion_rate"]
)

c3.metric(
    "Queue Depth",
    metrics["queue_depth"]
)

c4.metric(
    "Abandonment %",
    metrics["abandonment_rate"]
)

st.divider()

st.subheader("Zone Dwell Time")

if metrics["avg_dwell_per_zone"]:
    st.bar_chart(
        metrics["avg_dwell_per_zone"]
    )
else:
    st.info(
        "No dwell data available"
    )

st.divider()

st.subheader("Active Anomalies")

if anomalies["anomalies"]:

    for a in anomalies["anomalies"]:

        st.warning(
            f"{a['type']} | {a['severity']}"
        )

else:

    st.success(
        "No anomalies detected"
    )

st.divider()

st.subheader("Raw Metrics")

st.json(metrics)