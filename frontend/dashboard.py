# command to run the streamlit --> python -m streamlit run app.py

import time
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import data_provider as dp

st.set_page_config(page_title="TrafficMind", page_icon="🚦", layout="wide")

st.title("🚦 TrafficMind: Live Congestion Prediction")

# ---------- Sidebar Controls ----------
model = "XGBoost"
view = st.sidebar.radio("Map shows", ["Current", "Predicted"])
live = st.sidebar.checkbox("Live replay (updates every 2 sec)")

if "step" not in st.session_state:
    st.session_state.step = 0

st.write(f"Showing **{model}** AI Traffic Speed Forecast ({view} View)")

# ---------- Fetch Data from Provider ----------
step = st.session_state.step
sensors_df = dp.get_sensor_locations()
speed = dp.get_sensor_speeds(step=step, view=view, live=live)
anomalies, congested = dp.get_incident_alerts(speed)

# ---------- Top KPI Metric Cards ----------
c1, c2, c3 = st.columns(3)
c1.metric("Average Speed", f"{speed.mean():.0f} mph")
c2.metric("Congested Sensors", len(congested))
c3.metric("Accident Anomalies", len(anomalies), delta="Severe" if anomalies else "None", delta_color="inverse")

# ---------- Map & Alerts Layout ----------
col_left, col_right = st.columns([2, 1])

with col_left:
    m = folium.Map(location=[34.05, -118.25], zoom_start=11)
    for i, row in sensors_df.iterrows():
        s_val = speed[i]
        color, status = dp.classify_sensor_status(s_val)
        folium.CircleMarker(
            [row["lat"], row["lon"]],
            radius=9,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"Sensor {i}: {s_val} mph ({status})",
tooltip=f"Sensor {i}",
        ).add_to(m)

    m.fit_bounds([[sensors_df["lat"].min(), sensors_df["lon"].min()], [sensors_df["lat"].max(), sensors_df["lon"].max()]])
    st_folium(m, height=480, use_container_width=True)

with col_right:
    st.subheader("⚠️ Real-Time Alerts")
    if not anomalies and not congested:
        st.success("✅ Normal traffic flow — No anomalies detected")
    else:
        for i in anomalies:
            st.error(f"🚨 Sensor {i}: Accident-like sudden speed drop ({speed[i]} mph)")
        for i in congested:
            st.warning(f"⚠️ Sensor {i}: Congestion slowdown ({speed[i]} mph)")

    st.subheader("⏱️ Travel Time Estimate")
    route = st.multiselect("Choose sensors on route", list(range(len(sensors_df))), default=[0, 1, 2])
    eta = dp.estimate_route_eta(route, speed)
    st.metric("Estimated travel time", f"{eta:.0f} min")

# ---------- Speed Charts Section ----------
st.divider()
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Current Speed by Sensor")
    chart_data = pd.DataFrame({"Speed (mph)": speed}, index=[f"S{i:02d}" for i in range(len(sensors_df))])
    st.bar_chart(chart_data)

with col_chart2:
    st.subheader("📈 Time Series: Actual vs Predicted")
    selected_sensor = st.selectbox("Select sensor to inspect", [f"Sensor {i}" for i in range(len(sensors_df))], index=7)
    s_idx = int(selected_sensor.split()[1])

    trend_df = dp.get_sensor_speed_trend(s_idx, model, speed[s_idx])
    st.line_chart(trend_df)

# ---------- Evaluation Benchmarks ----------
st.divider()
eval_c1, eval_c2 = st.columns(2)

with eval_c1:
    st.subheader("📊 XGBoost: Speed Prediction vs Baseline")
    st.caption("Lower MAE and RMSE mean better predictions. The baseline is the simple historical average.")
    st.dataframe(dp.get_model_evaluation_metrics(), use_container_width=True, hide_index=True)

with eval_c2:
    st.subheader("🚨 Isolation Forest: Anomaly Detection vs Z-Score")
    st.caption("Precision means few false alarms. Recall means few missed incidents. Delay means how fast it alerts.")
    st.dataframe(dp.get_anomaly_evaluation_metrics(), use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("🗂️ K-Means: Congestion Levels")
    st.caption("K-Means groups real-time traffic observations into congestion levels based on speed patterns.")
    st.dataframe(dp.get_kmeans_summary(), use_container_width=True, hide_index=True)

# ---------- Live Replay Trigger ----------
if live:
    time.sleep(2)
    st.session_state.step += 1
    st.rerun()
