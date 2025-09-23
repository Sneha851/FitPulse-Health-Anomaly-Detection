import streamlit as st
import pandas as pd
import plotly.express as px
from data import sample_data  # single dataset with heart, sleep, steps, calories

# =========================
# Page Setup
# =========================
st.set_page_config(page_title="FitPulse - Health Dashboard", layout="wide")

# =========================
# Custom Styling
# =========================
st.markdown("""
    <style>
        .stApp { background: linear-gradient(to right, #f9f9f9, #e6f7ff); font-family: 'Segoe UI', sans-serif; }
        h1 { color: #1a5276; text-align: center; font-weight: bold; padding: 10px; }
        .metric-card { background: white; padding: 15px; border-radius: 15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); text-align: center; margin: 10px; }
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

# Navigation
page = st.sidebar.radio("📌 Navigation", ["Dashboard", "Heart Rate", "Sleep", "Steps", "Calories"])

# Threshold sliders
st.sidebar.subheader("⚙️ Threshold Controls")
hr_threshold = st.sidebar.slider("Heart Rate Threshold (bpm)", 60, 150, 120)
sleep_eff_threshold = st.sidebar.slider("Sleep Efficiency Threshold (%)", 50, 100, 75)

# Quick stats
df = pd.DataFrame(sample_data)
st.sidebar.metric("📈 Total Records", len(df))
st.sidebar.metric("📅 Date Range", f"{df['date'].min()} → {df['date'].max()}")

# =========================
# Main Page
# =========================
st.title("💓 FitPulse Health Dashboard")

# -------------------
# Dashboard Overview
# -------------------
if page == "Dashboard":
    st.subheader("📊 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg HR", f"{df['heart_rate'].mean():.1f} bpm")
    with col2:
        st.metric("Max HR", f"{df['heart_rate'].max()} bpm")
    with col3:
        st.metric("Avg Sleep", f"{df['sleep_hours'].mean():.1f} hrs")
    with col4:
        st.metric("Total Steps", f"{df['steps'].sum():.0f}")
    
    # Heart Rate chart
    st.subheader("📈 Heart Rate Trend")
    fig_hr = px.line(df, x='date', y='heart_rate', title="Heart Rate Over Time", markers=True)
    st.plotly_chart(fig_hr, use_container_width=True)
    
    # Sleep chart
    st.subheader("😴 Sleep Trend")
    fig_sleep = px.bar(df, x='date', y='sleep_hours', title="Sleep Hours Per Day")
    st.plotly_chart(fig_sleep, use_container_width=True)
    
    # Steps chart
    st.subheader("👟 Steps Trend")
    fig_steps = px.area(df, x='date', y='steps', title="Steps Over Time")
    st.plotly_chart(fig_steps, use_container_width=True)
    
    # Calories chart
    st.subheader("🔥 Calories Burned")
    fig_cal = px.area(df, x='date', y='calories', title="Calories Burned Over Time")
    st.plotly_chart(fig_cal, use_container_width=True)

# -------------------
# Heart Rate Page
# -------------------
elif page == "Heart Rate":
    df['hr_anomaly'] = df['heart_rate'] > hr_threshold
    st.subheader("📈 Heart Rate Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg HR", f"{df['heart_rate'].mean():.1f} bpm")
    with col2:
        st.metric("Max HR", f"{df['heart_rate'].max()} bpm")
    
    fig_hr = px.line(df, x='date', y='heart_rate', title="Heart Rate Trend")
    fig_hr.add_scatter(
        x=df[df['hr_anomaly']]['date'],
        y=df[df['hr_anomaly']]['heart_rate'],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Anomaly'
    )
    st.plotly_chart(fig_hr, use_container_width=True)

# -------------------
# Sleep Page
# -------------------
elif page == "Sleep":
    df['total_sleep'] = df['sleep_hours']
    df['sleep_anomaly'] = df['total_sleep'] < (sleep_eff_threshold / 12)  # simple check
    st.subheader("💤 Sleep Analysis")
    st.line_chart(df.set_index('date')['sleep_hours'])
    
# -------------------
# Steps Page
# -------------------
elif page == "Steps":
    st.subheader("👟 Steps Analysis")
    st.area_chart(df.set_index('date')['steps'])

# -------------------
# Calories Page
# -------------------
elif page == "Calories":
    st.subheader("🔥 Calories Burned")
    st.area_chart(df.set_index('date')['calories'])
