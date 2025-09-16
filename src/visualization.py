import matplotlib.pyplot as plt

def plot_anomalies(df, time_column, value_column):
    """Plot normal vs anomaly points"""
    plt.figure(figsize=(12,6))
    normal = df[df['anomaly'] == 0]
    anomaly = df[df['anomaly'] == 1]

    plt.plot(normal[time_column], normal[value_column], label='Normal')
    plt.scatter(anomaly[time_column], anomaly[value_column], color='red', label='Anomaly')
    plt.xlabel("Time")
    plt.ylabel(value_column)
    plt.title(f"Anomaly Detection in {value_column}")
    plt.legend()
    plt.show()
