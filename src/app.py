import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page config ---
st.set_page_config(page_title="FitPulse Anomaly Detection", page_icon="⚡", layout="wide")

# --- Styles ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        color: #333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stFileUploader>div>div>input {
        border: 2px dashed #4CAF50;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ FitPulse Health Anomaly Detection")
st.markdown("Upload your CSV with heart rate or related features to detect anomalies.")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Choose CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV Loaded Successfully!")
        st.write("### Dataset Preview", df.head())
        st.write("### Columns in Dataset", df.columns.tolist())
        st.write(f"**Shape:** {df.shape}  |  **Size:** {df.size}")
        
        # --- Select numeric column ---
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not numeric_cols:
            st.error("No numeric columns found for anomaly detection.")
        else:
            hr_column = st.selectbox("Select column for anomaly detection", numeric_cols)

            # --- Threshold slider ---
            threshold = st.slider("Z-score Threshold for anomaly detection", 0.5, 5.0, 3.0, 0.1)

            # --- Detect anomalies ---
            data = df[hr_column]
            mean_val = data.mean()
            std_val = data.std()
            z_score = (data - mean_val) / std_val
            anomalies = df[np.abs(z_score) > threshold]

            st.write(f"⚠️ Number of anomalies detected: {anomalies.shape[0]}")

            # --- Plot ---
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(data.index, data, label="Original Data", color="blue")
            ax.scatter(anomalies.index, anomalies[hr_column], color="red", label="Anomalies")
            ax.set_xlabel("Index")
            ax.set_ylabel(hr_column)
            ax.set_title("📈 Anomaly Detection Plot")
            ax.legend()
            st.pyplot(fig)

            # --- Download anomalies ---
            st.download_button(
                label="Download Anomalies CSV",
                data=anomalies.to_csv(index=False),
                file_name="anomalies.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error reading file: {e}")
