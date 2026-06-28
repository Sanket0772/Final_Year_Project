import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from RAG.chatbot import ask_question
import requests
import plotly.graph_objects as go
from datetime import datetime

# Auto refresh every 5 sec
if "chat_busy" not in st.session_state:
    st.session_state.chat_busy = False

if not st.session_state.chat_busy:
    st_autorefresh(interval=5000, key="refresh")

st.set_page_config(
    page_title="AI Predictive Maintenance Dashboard",
    layout="wide"
)


API_URL = "http://127.0.0.1:8000"

def fetch_history():
    try:
        response = requests.get(f"{API_URL}/history", timeout=5)
        response.raise_for_status()
        return pd.DataFrame(response.json())

    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to FastAPI:\n{e}")
        st.stop()

df = fetch_history()

if df.empty:
    st.warning("No sensor data available.")
    st.stop()



st.sidebar.header("Dashboard Controls")

anomaly_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=df["anomaly"].unique(),
    default=df["anomaly"].unique()
)

df = df[df["anomaly"].isin(anomaly_filter)]

st.markdown("""
<style>

.metric-container{
background:#1f2937;
padding:10px;
border-radius:10px;
}

</style>
""",unsafe_allow_html=True)

st.title("Live AI Predictive Maintenance Dashboard")
st.markdown("Real-time anomaly monitoring")

total_records = len(df)
anomaly_count = len(df[df["anomaly"] == "Anomaly"])
normal_count = len(df[df["anomaly"] == "Normal"])

health_score = round((normal_count / total_records) * 100, 2)

latest = df.iloc[0]
failure_risk = latest.get("failure_risk", 0)


rpm = latest["rpm"]
temp = latest["outlet_temp"]
pressure = latest["outlet_pressure_bar"]
airflow = latest["air_flow"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Health Score", f"{health_score}%")
col2.metric("RPM", f"{rpm:.0f}")
col3.metric("Temperature", f"{temp:.1f} °C")
col4.metric("Pressure", f"{pressure:.2f} bar")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Records", total_records)
col6.metric("Normal", normal_count)
col7.metric("Anomalies", anomaly_count)
col8.metric("Air Flow", f"{airflow:.1f}")

st.subheader("Failure Assessment")

st.sidebar.success("FastAPI Connected")
st.sidebar.markdown("---")

st.sidebar.subheader("Current Time")

current_time = datetime.now().strftime("%H:%M:%S")

st.sidebar.info(current_time)

st.sidebar.subheader("Last Update")

st.sidebar.success(
    latest["timestamp"]
)

st.sidebar.metric(
    "Health Score",
    f"{health_score}%"
)

st.sidebar.metric(
    "Failure Risk",
    f"{failure_risk}%"
)

risk_col1, risk_col2 = st.columns(2)

risk_col1.metric(
    "Failure Risk",
    f"{failure_risk:.1f}%"
)

risk_col2.metric(
    "Machine Status",
    "Critical" if failure_risk > 70
    else "Warning" if failure_risk > 40
    else "Healthy"
)
st.subheader("Live Sensor Trends")

col1, col2 = st.columns(2)

with col1:

    fig_temp = px.line(
        df.sort_values("id"),
        x="id",
        y="outlet_temp",
        title="Temperature Trend"
    )

    st.plotly_chart(fig_temp, use_container_width=True)

with col2:

    fig_rpm = px.line(
        df.sort_values("id"),
        x="id",
        y="rpm",
        title="RPM Trend"
    )

    st.plotly_chart(fig_rpm, use_container_width=True)

col3, col4 = st.columns(2)

with col3:

    fig_health = px.line(
        df.sort_values("id"),
        x="id",
        y="health_score",
        title="Health Score Trend"
    )

    st.plotly_chart(fig_health, use_container_width=True)

with col4:

    fig_failure = px.line(
        df.sort_values("id"),
        x="id",
        y="failure_risk",
        title="Failure Risk Trend"
    )

    st.plotly_chart(fig_failure, use_container_width=True)

st.subheader("System Status Distribution")

col1, col2 = st.columns(2)

with col1:

    status_counts = (
        df["anomaly"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig_pie = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Normal vs Anomaly Distribution",
        hole=0.45
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


with col2:

    fig_air = px.line(
        df.sort_values("id"),
        x="id",
        y="air_flow",
        title="Air Flow Trend"
    )

    st.plotly_chart(
        fig_air,
        use_container_width=True
    )

st.subheader("Sensor Correlation Heatmap")

corr = df[
    [
        "rpm",
        "motor_power",
        "torque",
        "outlet_pressure_bar",
        "air_flow",
        "noise_db",
        "outlet_temp",
        "water_flow",
        "failure_risk",
        "health_score"
    ]
].corr()

fig_heat = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=corr.round(2).values,
        texttemplate="%{text}",
        colorscale="RdBu",
        zmin=-1,
        zmax=1
    )
)

fig_heat.update_layout(
    height=650
)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)




def get_recommendations(row):

    recommendations = []

    if row["rpm"] < 900:
        recommendations.append("Inspect motor bearings.")

    if row["outlet_temp"] > 60:
        recommendations.append("Check cooling system.")

    if row["noise_db"] > 85:
        recommendations.append("Inspect rotor alignment.")

    if row["water_flow"] < 20:
        recommendations.append("Inspect water circulation.")

    if not recommendations:
        recommendations.append("System operating normally.")

    return recommendations

st.subheader("Maintenance Recommendations")

for rec in get_recommendations(latest):
    st.info(rec)


if anomaly_count > 0:
    st.error("⚠️ Live anomaly detected!")
else:
    st.success("Machine healthy")

col5, col6 = st.columns(2)

with col5:
    fig1 = px.scatter(
        df,
        x="rpm",
        y="outlet_temp",
        color="anomaly"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    fig2 = px.line(
        df.sort_values("id"),
        x="id",
        y="motor_power",
        color="anomaly"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.dataframe(df, use_container_width=True)





# Chatbot Section 


# Chatbot Section
st.subheader("AI Maintenance Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_query = st.chat_input("Ask about the dehumidifier...")

if user_query:
    st.session_state.chat_busy = True

    # store user message first
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    # show user message
    with st.chat_message("user"):
        st.write(user_query)

    # get chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_question(user_query)
            st.write(response)

    # store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.chat_busy = False