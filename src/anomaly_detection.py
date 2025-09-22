import pandas as pd
import numpy as np

def detect_anomalies(df, column='HR', threshold=1.5):
    mean_val = df[column].mean()
    std_val = df[column].std()
    df['Anomaly'] = np.where(np.abs(df[column] - mean_val) > threshold * std_val, 1, 0)
    return df
