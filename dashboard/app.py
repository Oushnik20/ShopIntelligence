import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Store Intelligence",
    page_icon="🏪",
    layout="wide"
)

API_URL = "https://shopintelligence.onrender.com"
STORE_ID = "STORE_BLR_002"

try:

    metrics = requests.get(
        f"{API_URL}/stores/{STORE_ID}/metrics",
        timeout=15
    ).json()

    anomalies = requests.get(
        f"{API_URL}/stores/{STORE_ID}/anomalies",
        timeout=15
    ).json()

    funnel = requests.get(
        f"{API_URL}/stores/{STORE_ID}/funnel",
        timeout=15
    ).json()

except Exception as e:

    st.error(
        f"Backend connection failed: {e}"
    )

    st.stop()

st.title("🏪 Store Intelligence Platform")
st.caption(
    "AI-Powered Retail Analytics Dashboard"
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Visitors",
        metrics["unique_visitors"]
    )

with col2:
    st.metric(
        "💰 Conversion %",
        f"{metrics['conversion_rate']}%"
    )

with col3:
    st.metric(
        "🛒 Queue Depth",
        metrics["queue_depth"]
    )

with col4:
    st.metric(
        "⚠️ Abandonment %",
        f"{metrics['abandonment_rate']}%"
    )

st.markdown(
    """
    Monitor visitor engagement, dwell time,
    queue performance, conversion funnel,
    and operational anomalies across the store.
    """
)

st.divider()

st.subheader("📈 Conversion Funnel")

funnel_df = pd.DataFrame(
    {
        "Stage": [
            "Entry",
            "Zone Visit",
            "Billing Queue",
            "Purchase"
        ],
        "Visitors": [
            funnel["entry"],
            funnel["zone_visit"],
            funnel["billing_queue"],
            funnel["purchase"]
        ]
    }
)

st.bar_chart(
    funnel_df.set_index("Stage")
)

st.divider()

st.subheader("⏱ Zone Dwell Time")

if metrics["avg_dwell_per_zone"]:

    dwell_df = pd.DataFrame(
        {
            "Zone": list(
                metrics["avg_dwell_per_zone"].keys()
            ),
            "Seconds": list(
                metrics["avg_dwell_per_zone"].values()
            )
        }
    )

    st.bar_chart(
        dwell_df.set_index("Zone")
    )

else:

    st.info(
        "No dwell data available"
    )

st.divider()

st.subheader("🚨 Active Anomalies")

if anomalies["anomalies"]:

    for a in anomalies["anomalies"]:

        st.warning(
            f"""
Type: {a['type']}

Severity: {a['severity']}

Suggested Action: {a['suggested_action']}
"""
        )

else:

    st.success(
        "No anomalies detected"
    )

st.divider()

with st.expander(
    "🔍 View Raw Metrics"
):
    st.json(metrics)

with st.expander(
    "🔍 View Funnel Data"
):
    st.json(funnel)

with st.expander(
    "🔍 View Anomaly Data"
):
    st.json(anomalies)

st.divider()

st.caption(
    "Store Intelligence Platform"
)