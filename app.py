import os
import pandas as pd
import streamlit as st

# Page Configuration with Custom Styling
st.set_page_config(
    page_title="Ukraine Protection Tracker - Greece",
    page_icon="🇺🇦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for UI Enhancement
st.markdown(
    """
    <style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        font-weight: 600;
        color: #495057;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #0d6efd;
    }
    </style>
""",
    unsafe_allow_keywords=True,
)

# 1. Locate and Load Dataset
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]

if not csv_files:
    st.error("No .csv file found in the repository folder.")
    st.stop()

csv_path = os.path.join(dir_path, csv_files[0])
df = pd.read_csv(csv_path)

# Position-based Column Normalization
if len(df.columns) >= 4:
    df.columns = ["year_month", "female", "male", "total"] + list(
        df.columns[4:]
    )
else:
    df.columns = df.columns.str.strip().str.lower()

# Clean Numeric Data
for col in ["female", "male", "total"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# --- SIDEBAR FILTERS ---
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Greece.svg",
    width=60,
)
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown(
    "Filter dataset timeframe and customize visualization settings."
)

# Date Range Filter
unique_dates = df["year_month"].unique().tolist()
selected_dates = st.sidebar.select_slider(
    "Select Time Horizon:",
    options=unique_dates,
    value=(unique_dates[0], unique_dates[-1]),
)

# Filter Dataframe based on Slider
start_idx = unique_dates.index(selected_dates[0])
end_idx = unique_dates.index(selected_dates[1])
filtered_df = df.iloc[start_idx : end_idx + 1]

st.sidebar.markdown("---")
st.sidebar.info(
    "**Data Source:** Eurostat (`migr_asytpfm`)\n\n"
    "**Target Country:** Greece 🇬🇷\n\n"
    "**Beneficiaries:** Citizens of Ukraine 🇺🇦"
)

# --- MAIN DASHBOARD HEADER ---
st.title("🇺🇦 Temporary Protection Tracker: Greece")
st.caption(
    "Interactive analytics on Ukrainian refugees granted Temporary Protection"
    f" status in Greece ({selected_dates[0]} to {selected_dates[1]})."
)

st.markdown("---")

# --- TOP METRIC CARDS ---
latest = filtered_df.iloc[-1]
previous = (
    filtered_df.iloc[-2]
    if len(filtered_df) > 1
    else filtered_df.iloc[-1]
)

# Calculate Monthly Deltas
total_delta = int(latest["total"] - previous["total"])
female_delta = int(latest["female"] - previous["female"])
male_delta = int(latest["male"] - previous["male"])

c1, c2, c3 = st.columns(3)
c1.metric(
    "Total Beneficiaries",
    f"{latest['total']:,}",
    delta=f"{total_delta:+,} vs prev. month",
)
c2.metric(
    "Female Beneficiaries",
    f"{latest['female']:,}",
    delta=f"{female_delta:+,} vs prev. month",
)
c3.metric(
    "Male Beneficiaries",
    f"{latest['male']:,}",
    delta=f"{male_delta:+,} vs prev. month",
)

st.markdown("<br>", unsafe_allow_keywords=True)

# --- VISUALIZATIONS SECTION ---
tab1, tab2 = st.tabs(["📈 Trend Analysis", "📊 Gender Distribution"])

with tab1:
    st.subheader("Beneficiaries Growth Over Time")
    st.line_chart(
        filtered_df.set_index("year_month")[["total", "female", "male"]],
        color=["#0d6efd", "#dc3545", "#198754"],
    )

with tab2:
    st.subheader("Latest Gender Ratio Breakdown")
    if latest["total"] > 0:
        female_pct = (latest["female"] / latest["total"]) * 100
        male_pct = (latest["male"] / latest["total"]) * 100

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Female Ratio", f"{female_pct:.1f}%")
            st.progress(female_pct / 100)
        with col_b:
            st.metric("Male Ratio", f"{male_pct:.1f}%")
            st.progress(male_pct / 100)

st.markdown("---")

# --- DATASET TABLE & EXPORT ---
st.subheader("📋 Underlying Dataset")

col_left, col_right = st.columns([3, 1])
with col_left:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with col_right:
    # CSV Download Button
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv_data,
        file_name="ukraine_protection_greece_filtered.csv",
        mime="text/csv",
    )
