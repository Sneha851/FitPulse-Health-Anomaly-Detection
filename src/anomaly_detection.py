from sklearn.ensemble import IsolationForest

def detect_anomalies(df, value_column):
    """Detect anomalies using Isolation Forest"""
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[[value_column]])
    df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})  # 0=normal, 1=anomaly
    return df
