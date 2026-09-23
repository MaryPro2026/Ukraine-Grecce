import os
import pandas as pd
import streamlit as st

# Page Setup
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

# 1. Locate file path safely
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path, "ukraine_greece.csv")

# Verify file existence
if not os.path.exists(csv_path):
    st.error(f"Cannot find 'ukraine_greece.csv' in folder: {dir_path}")
    st.stop()

# 2. Load Data
df = pd.read_csv(csv_path)

# Clean column headers (strip spaces and force lowercase)
df.columns = df.columns.str.strip().str.lower()

# Convert numeric columns safely
for col in ["female", "male", "total"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# 3. KPI Metrics
latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Beneficiaries", f"{latest['total']:,}")
col2.metric("Females", f"{latest['female']:,}")
col3.metric("Males", f"{latest['male']:,}")

st.markdown("---")

# 4. Visualizations
st.subheader("📈 Trend over Time")
st.line_chart(df.set_index("year_month")[["total", "female", "male"]])

st.subheader("📊 Latest Gender Breakdown")
if latest["total"] > 0:
    female_pct = (latest["female"] / latest["total"]) * 100
    st.progress(female_pct / 100)
    st.caption(f"Female: **{female_pct:.1f}%** | Male:"
        f" **{(100 - female_pct):.1f}%**")
st.markdown("---")
# 5. Data Table
st.subheader("📋 Dataset")
st.dataframe(df, use_container_width=True)
