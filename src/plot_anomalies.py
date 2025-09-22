import matplotlib.pyplot as plt
import seaborn as sns

def plot_anomalies(df, column='HR'):
    plt.figure(figsize=(12,6))
    sns.lineplot(x=df.index, y=df[column], label='Heart Rate')
    anomalies = df[df['Anomaly'] == 1]
    sns.scatterplot(x=anomalies.index, y=anomalies[column], color='red', label='Anomaly')
    plt.title("Heart Rate Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Heart Rate")
    plt.legend()
    plt.tight_layout()
    return plt
