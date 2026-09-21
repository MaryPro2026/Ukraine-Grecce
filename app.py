import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Ukraine Protection Tracker - Greece",
    page_icon="🇺🇦",
    layout="wide",
)

# Title & Description
st.title("🇺🇦 Temporary Protection Beneficiaries in Greece")
st.write(
    "Tracking Ukrainian refugees under Temporary Protection status in Greece"
    " based on official Eurostat data."
)

# 1. Get the directory path where app.py is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# 2. Automatically find any CSV file in that directory
csv_files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]

if not csv_files:
    st.error(
        "No CSV file found in the GitHub repository. Please upload your"
        " dataset."
    )
    st.stop()

# 3. Load the CSV file automatically
csv_path = os.path.join(dir_path, csv_files[0])
df = pd.read_csv(csv_path)
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
import os
import pandas as pd
import streamlit as st

# Page Configuration
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

# 1. Locate the CSV file in the repository
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]

if not csv_files:
    st.error("No CSV file found in the repository. Please upload your dataset.")
    st.stop()

csv_path = os.path.join(dir_path, csv_files[0])
df = pd.read_csv(csv_path)

# 2. Clean and standardize column names (lowercase, remove spaces)
df.columns = df.columns.str.strip().str.lower()

# Map common column name variations
col_mapping = {
    "total_beneficiaries": "total",
    "t": "total",
    "women": "female",
    "f": "female",
    "men": "male",
    "m": "male",
    "time_period": "year_month",
}
df = df.rename(columns=col_mapping)

# Check if required columns exist
required_cols = ["year_month", "female", "male", "total"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing columns in CSV: {missing_cols}")
    st.write("Found columns in your CSV:", list(df.columns))
    st.stop()

# 3. Display KPI Metrics for the latest month
latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Beneficiaries", f"{int(latest['total']):,}")
col2.metric("Females", f"{int(latest['female']):,}")
col3.metric("Males", f"{int(latest['male']):,}")

st.markdown("---")

# 4. Line Chart - Overall Trend
st.subheader("📈 Trend over Time")
st.line_chart(df.set_index("year_month")[["total", "female", "male"]])

# 5. Gender Breakdown Progress Bar
st.subheader("📊 Latest Gender Breakdown")
female_pct = (latest["female"] / latest["total"]) * 100
male_pct = (latest["male"] / latest["total"]) * 100

st.progress(female_pct / 100)
st.caption(f"Female: **{female_pct:.1f}%** | Male: **{male_pct:.1f}%**")

st.markdown("---")

# 6. Raw Data Table
st.subheader("📋 Dataset")
st.dataframe(df, use_container_width=True)
