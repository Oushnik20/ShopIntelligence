import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Store Intelligence",
    page_icon="🏪",
    layout="wide"
)

STORE_ID = "STORE_BLR_002"

metrics = requests.get(
    f"http://localhost:8000/stores/{STORE_ID}/metrics"
).json()

anomalies = requests.get(
    f"http://localhost:8000/stores/{STORE_ID}/anomalies"
).json()

funnel = requests.get(
    f"http://localhost:8000/stores/{STORE_ID}/funnel"
).json()

st.title("Store Intelligence Platform")
st.caption("Retail Analytics Dashboard")

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
    Monitor visitor engagement, queue health,
    conversion performance and store anomalies.
    """
)

st.divider()

st.subheader("Conversion Funnel")

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

st.subheader("Active Anomalies")

if anomalies["anomalies"]:

    for a in anomalies["anomalies"]:

        st.warning(
            f"""
{a['type']}

Severity: {a['severity']}

Action: {a['suggested_action']}
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