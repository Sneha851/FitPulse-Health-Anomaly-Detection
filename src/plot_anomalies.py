import pandas as pd
import matplotlib.pyplot as plt

# Load the anomaly CSV
df = pd.read_csv("data/heartrate_with_anomalies.csv")

# Plot MEAN_RR with anomalies highlighted
plt.figure(figsize=(12,6))
plt.plot(df['MEAN_RR'], label='MEAN_RR')
plt.scatter(df.index[df['anomaly']==1], df['MEAN_RR'][df['anomaly']==1], color='red', label='Anomaly')
plt.xlabel("Index")
plt.ylabel("MEAN_RR")
plt.title("Heart Rate Anomalies")
plt.legend()
plt.show()
