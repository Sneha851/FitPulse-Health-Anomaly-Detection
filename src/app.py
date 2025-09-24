import streamlit as st
import pandas as pd
import plotly.express as px
from data import sample_data  # fallback sample dataset

# =========================
# Page Setup
# =========================
st.set_page_config(page_title="FitPulse Health Dashboard", layout="wide")

# =========================
# Custom Styling
# =========================
st.markdown("""
    <style>
        .stApp { background: linear-gradient(to right, #f9f9f9, #e6f7ff); font-family: 'Segoe UI', sans-serif; }
        h1 { color: #1a5276; text-align: center; font-weight: bold; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
st.sidebar.markdown("""
<div style="background-color:#ffffff;
            padding:15px;
            border-radius:15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            text-align:center;">
    <img src="https://cdn-icons-png.flaticon.com/512/6997/6997662.png"
         width="80" style="border-radius:50%;">
    <h3 style="margin-bottom:0;">User: Sneha</h3>
    <p style="font-size:13px; color:gray;">Health Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------------
# Navigation
# ---------------------
page = st.sidebar.radio("📌 Navigation", ["Dashboard", "Heart Rate", "Sleep", "Steps", "Calories"])

# ---------------------
# File Uploader
# ---------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV dataset", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.DataFrame(sample_data)

# ---------------------
# Threshold Sliders (Reactive)
# ---------------------
hr_threshold = st.sidebar.slider("Heart Rate Threshold (bpm)", 60, 150, 120)
sleep_threshold = st.sidebar.slider("Sleep Hours Threshold", 3.0, 10.0, 6.0)

# =========================
# Dashboard Page
# =========================
if page == "Dashboard":
    st.title("📊 FitPulse Health Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg HR", f"{df['heart_rate'].mean():.1f} bpm")
    col2.metric("Max HR", f"{df['heart_rate'].max()} bpm")
    col3.metric("Avg Sleep", f"{df['sleep_hours'].mean():.1f} hrs")
    col4.metric("Total Steps", f"{df['steps'].sum():.0f}")

    st.subheader("📈 Heart Rate Trend")
    df['hr_anomaly'] = (df['heart_rate'] > hr_threshold)
    fig_hr = px.line(df, x='date', y='heart_rate', markers=True)
    fig_hr.add_scatter(x=df[df['hr_anomaly']]['date'], y=df[df['hr_anomaly']]['heart_rate'],
                       mode='markers', marker=dict(color='red', size=10), name='Anomaly')
    st.plotly_chart(fig_hr, use_container_width=True)

    st.subheader("😴 Sleep Trend")
    df['sleep_anomaly'] = (df['sleep_hours'] < sleep_threshold)
    fig_sleep = px.bar(df, x='date', y='sleep_hours', color=df['sleep_anomaly'].map({True:'red', False:'blue'}))
    st.plotly_chart(fig_sleep, use_container_width=True)

    st.subheader("👟 Steps Trend")
    fig_steps = px.area(df, x='date', y='steps', title="Steps Over Time")
    st.plotly_chart(fig_steps, use_container_width=True)

    st.subheader("🔥 Calories Burned")
    fig_cal = px.area(df, x='date', y='calories', title="Calories Burned Over Time")
    st.plotly_chart(fig_cal, use_container_width=True)

# =========================
# Heart Rate Page
# =========================
elif page == "Heart Rate":
    df['hr_anomaly'] = (df['heart_rate'] > hr_threshold)
    st.subheader("📈 Heart Rate Analysis")
    st.metric("Avg HR", f"{df['heart_rate'].mean():.1f} bpm")
    st.metric("Max HR", f"{df['heart_rate'].max()} bpm")
    fig = px.line(df, x='date', y='heart_rate', markers=True)
    fig.add_scatter(x=df[df['hr_anomaly']]['date'], y=df[df['hr_anomaly']]['heart_rate'],
                    mode='markers', marker=dict(color='red', size=10), name='Anomaly')
    st.plotly_chart(fig, use_container_width=True)

# =========================
# Sleep Page
# =========================
elif page == "Sleep":
    df['sleep_anomaly'] = df['sleep_hours'] < sleep_threshold
    st.subheader("😴 Sleep Analysis")
    fig = px.bar(df, x='date', y='sleep_hours', color=df['sleep_anomaly'].map({True:'red', False:'blue'}))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# Steps Page
# =========================
elif page == "Steps":
    st.subheader("👟 Steps Analysis")
    fig = px.area(df, x='date', y='steps')
    st.plotly_chart(fig, use_container_width=True)

# =========================
# Calories Page
# =========================
elif page == "Calories":
    st.subheader("🔥 Calories Burned")
    fig = px.area(df, x='date', y='calories')
    st.plotly_chart(fig, use_container_width=True)
