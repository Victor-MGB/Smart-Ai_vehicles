import streamlit as st
import pandas as pd
import json
import plotly.express as px
import folium
import requests
from streamlit_folium import folium_static

# ----------------------------
# 🚀 APP CONFIG
# ----------------------------
st.set_page_config(
    page_title="Smart Transport Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 💅 CUSTOM STYLING
# ----------------------------
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #eef2f5;
        }
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #0d6efd;
        }
        .sub-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        section.main > div {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 📋 SIDEBAR
# ----------------------------
st.sidebar.image("https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/000000/external-transportation-transport-flaticons-lineal-color-flat-icons.png", width=60)
st.sidebar.title("🚗 Smart Transport Menu")
menu = st.sidebar.radio("Navigate", ["🛁 Live Sensor Data", "🛠️ Predictive Maintenance"])
st.sidebar.markdown("---")
st.sidebar.markdown("📁 Data: JSONL/CSV files")
st.sidebar.markdown("🔧 Powered by FastAPI")

# ----------------------------
# 🛁 LIVE SENSOR DATA SECTION
# ----------------------------
if menu == "🛁 Live Sensor Data":
    st.markdown("<div class='main-title'>🛁 Live Sensor Monitoring</div>", unsafe_allow_html=True)

    @st.cache_data
    def load_sensor_data(file_path: str):
        with open(file_path, "r") as f:
            lines = [json.loads(line) for line in f]
        return pd.json_normalize(lines)

    try:
        df = load_sensor_data("data/sensor_data_stream.jsonl")

        st.markdown("<div class='sub-title'>📄 Sensor Data Snapshot</div>", unsafe_allow_html=True)
        st.dataframe(df.head(50), use_container_width=True)

        st.markdown("<div class='sub-title'>📊 Sensor Metrics Overview</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            fig = px.histogram(df, x="battery.temperature", nbins=30, color_discrete_sequence=["#FFA500"])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.box(df, y="motor.vibration_level", points="all", color_discrete_sequence=["#1f77b4"])
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            errors = df["battery.error_code"].value_counts().reset_index()
            errors.columns = ["error_code", "count"]
            fig3 = px.bar(errors, x="error_code", y="count", color="error_code")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("<div class='sub-title'>📍 Component Locations & Detected Anomalies</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1.5, 1.5])

        with col1:
            m = folium.Map(location=[9.0820, 8.6753], zoom_start=6)
            for _, row in df.iterrows():
                lat = row.get("location.latitude")
                lon = row.get("location.longitude")
                if pd.notnull(lat) and pd.notnull(lon):
                    popup = f"""
                    <b>Component ID:</b> {row['component_id']}<br>
                    <b>Battery Temp:</b> {row['battery.temperature']} °C<br>
                    <b>Vibration:</b> {row['motor.vibration_level']}<br>
                    <b>Error:</b> {row['battery.error_code']}
                    """
                    icon_color = "red" if row["battery.error_code"] != "OK" else "green"
                    folium.Marker(
                        location=[lat, lon],
                        popup=popup,
                        icon=folium.Icon(color=icon_color)
                    ).add_to(m)
            folium_static(m)

        with col2:
            df["anomaly_flag"] = ((df["battery.temperature"] > 85) & (df["motor.vibration_level"] > 1.0)).astype(int)
            anomaly_df = df.groupby(pd.to_datetime(df["timestamp"]).dt.date)["anomaly_flag"].sum().reset_index()
            anomaly_df.columns = ["date", "anomalies"]
            fig_anomaly = px.line(anomaly_df, x="date", y="anomalies", title="🚨 Daily Anomalies")
            st.plotly_chart(fig_anomaly, use_container_width=True)

    except FileNotFoundError:
        st.warning("⚠️ File not found: `data/sensor_data_stream.jsonl`")

# ----------------------------
# 🛠️ PREDICTIVE MAINTENANCE SECTION
# ----------------------------
elif menu == "🛠️ Predictive Maintenance":
    st.markdown("<div class='main-title'>🛠️ Predictive Maintenance</div>", unsafe_allow_html=True)

    # 👇 Sidebar config sliders
    st.sidebar.markdown("### ⚙️ Decision Engine Settings")
    threshold = st.sidebar.slider("Failure Probability Threshold", 0.0, 1.0, 0.6, 0.05)
    cost_failure = st.sidebar.number_input("Expected Failure Cost", value=5000)
    early_fix_cost = st.sidebar.number_input("Early Fix Cost", value=1000)

    uploaded = st.file_uploader("📂 Upload CSV Sensor Data", type="csv")

    if uploaded:
        with st.spinner("⏳ Analyzing uploaded data..."):
            df_upload = pd.read_csv(uploaded)
            decisions = []

            for _, row in df_upload.iterrows():
                payload = {
                    "component_id": row["component_id"],
                    "battery_temperature": row["battery.temperature"],
                    "motor_vibration_level": row["motor.vibration_level"],
                    "error_flag": 1 if row["battery.error_code"] != "OK" else 0
                }

                try:
                    response = requests.post("http://localhost:8000/recommend-maintenance", json=payload)
                    result = response.json()
                except Exception as e:
                    st.error(f"⚠️ Backend error: {e}")
                    st.stop()

                result["latitude"] = row.get("location.latitude") or row.get("latitude")
                result["longitude"] = row.get("location.longitude") or row.get("longitude")
                result["component_id"] = row["component_id"]
                decisions.append(result)

            decision_df = pd.DataFrame(decisions)

        st.markdown("<div class='sub-title'>🧾 Raw Recommendations</div>", unsafe_allow_html=True)
        st.dataframe(decision_df, use_container_width=True)

        def recommend_action(prob, cost_failure, cost_fix, threshold=0.6):
            expected_failure_cost = prob * cost_failure
            decision = "FIX" if expected_failure_cost > cost_fix or prob >= threshold else "WAIT"
            reason = f"Expected cost: {expected_failure_cost:.2f} > fix cost: {cost_fix}" if decision == "FIX" else "Below threshold"
            return decision, reason

        def apply_decision_engine(sensor_df: pd.DataFrame, cost_config: dict, threshold=0.6):
            results = []
            for _, row in sensor_df.iterrows():
                decision, reason = recommend_action(
                    row['failure_probability'],
                    cost_config['cost_failure'],
                    cost_config['early_fix_cost'],
                    threshold
                )
                results.append({
                    "component_id": row['component_id'],
                    "vehicle_id": row.get('vehicle_id', 'N/A'),
                    "failure_probability": row['failure_probability'],
                    "decision": decision,
                    "explanation": reason,
                    "latitude": row.get("latitude"),
                    "longitude": row.get("longitude")
                })
            return pd.DataFrame(results)

        decision_engine_df = apply_decision_engine(decision_df, {
            "cost_failure": cost_failure,
            "early_fix_cost": early_fix_cost
        }, threshold)

        st.markdown(f"### 🤖 Actionable Recommendations (Threshold ≥ {threshold})")
        st.dataframe(decision_engine_df, use_container_width=True)

        summary = decision_engine_df['decision'].value_counts().reset_index()
        summary.columns = ['decision', 'count']
        fig_summary = px.bar(summary, x='decision', y='count', color='decision', title="🔍 FIX vs WAIT Decisions")
        st.plotly_chart(fig_summary, use_container_width=True)

        fix_df = decision_engine_df[decision_engine_df['decision'] == 'FIX']

        st.markdown("### 🧠 Filtered: Components Needing Immediate Attention")
        st.dataframe(fix_df, use_container_width=True)

        st.markdown("### 📍 Fix-Now Locations")
        map_fix = folium.Map(location=[6.5244, 3.3792], zoom_start=6)
        for _, row in fix_df.iterrows():
            if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=f"{row['component_id']} (Prob: {row['failure_probability']:.2f})",
                    icon=folium.Icon(color="red", icon="wrench", prefix="fa")
                ).add_to(map_fix)
        folium_static(map_fix)

        # 🔄 Animated Map with Plotly
        st.markdown("### 📍 Animated Map of FIX Components")
        if "timestamp" in fix_df.columns:
            fix_df["timestamp"] = pd.to_datetime(fix_df["timestamp"])
            fix_df["frame"] = fix_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        else:
            fix_df["frame"] = fix_df.index.astype(str)

        fig_animated = px.scatter_mapbox(
            fix_df,
            lat="latitude",
            lon="longitude",
            color="component_id",
            size="failure_probability",
            animation_frame="frame",
            zoom=5,
            height=600,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig_animated, use_container_width=True)

        # 📅 Download Report
        st.markdown("### 📅 Download Report")
        csv = fix_df.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download FIX Report (.csv)", data=csv, file_name="fix_now_report.csv", mime="text/csv")

    else:
        st.info("📁 Please upload a `.csv` file to proceed.")
