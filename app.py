import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Ukraine Protection Tracker - Greece",
    page_icon="🇺🇦",
    layout="wide",
)

st.title("🇺🇦 Temporary Protection Beneficiaries in Greece")
st.write(
    "Tracking Ukrainian refugees under Temporary Protection status in Greece"
    " based on official Eurostat data."
)

# Load Data
df = pd.read_csv("ukraine_greece.csv")

# Latest Month KPIs
latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Beneficiaries", f"{int(latest['total']):,}")
col2.metric("Females", f"{int(latest['female']):,}")
col3.metric("Males", f"{int(latest['male']):,}")

st.markdown("---")

# Trend Chart
st.subheader("📈 Trend over Time")
st.line_chart(df.set_index("year_month")[["total", "female", "male"]])

# Gender Breakdown Progress Bar
st.subheader("📊 Latest Gender Breakdown")
female_pct = (latest["female"] / latest["total"]) * 100
male_pct = (latest["male"] / latest["total"]) * 100

st.progress(female_pct / 100)
st.caption(f"Female: **{female_pct:.1f}%** | Male: **{male_pct:.1f}%**")

st.markdown("---")

# Data Table
st.subheader("📋 Dataset")
st.dataframe(df, use_container_width=True)
