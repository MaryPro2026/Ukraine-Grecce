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

# 1. Locate and load CSV file automatically
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]

if not csv_files:
    st.error("No .csv file found in the repository folder.")
    st.stop()

csv_path = os.path.join(dir_path, csv_files[0])
df = pd.read_csv(csv_path)

# 2. Force-rename columns based on position (Column 1=Date, 2=Female, 3=Male, 4=Total)
# This guarantees it works even if headers are misspelled or uppercase in the CSV
if len(df.columns) >= 4:
    df.columns = ["year_month", "female", "male", "total"] + list(
        df.columns[4:]
    )
else:
    # Fallback cleaning if less than 4 columns
    df.columns = df.columns.str.strip().str.lower()

# 3. Convert numeric columns safely
for col in ["female", "male", "total"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# 4. KPI Metrics
latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Beneficiaries", f"{latest['total']:,}")
col2.metric("Females", f"{latest['female']:,}")
col3.metric("Males", f"{latest['male']:,}")

st.markdown("---")

# 5. Visualizations
st.subheader("📈 Trend over Time")
st.line_chart(df.set_index("year_month")[["total", "female", "male"]])

st.subheader("📊 Latest Gender Breakdown")
if latest["total"] > 0:
    female_pct = (latest["female"] / latest["total"]) * 100
    st.progress(female_pct / 100)
    st.caption(
        f"Female: **{female_pct:.1f}%** | Male:"
        f" **{(100 - female_pct):.1f}%**"
    )

st.markdown("---")

# 6. Raw Data Table
st.subheader("📋 Dataset")
st.dataframe(df, use_container_width=True)
