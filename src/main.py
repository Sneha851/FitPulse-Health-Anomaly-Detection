import pandas as pd
from sklearn.ensemble import IsolationForest

# Load your CSV
df = pd.read_csv("data/heartrate_seconds.csv")

# Remove non-numeric columns
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
print("Numeric features used for anomaly detection:", numeric_cols)

X = df[numeric_cols]

# Fit Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = model.fit_predict(X)

# Convert anomaly output from -1/1 to 1=anomaly, 0=normal
df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)

# Save result
df.to_csv("data/heartrate_with_anomalies.csv", index=False)
print("Anomaly detection complete! Check heartrate_with_anomalies.csv")

