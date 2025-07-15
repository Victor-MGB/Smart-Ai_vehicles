import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Set seaborn theme
sns.set(style="whitegrid", palette="deep", font_scale=1.1)

def load_and_flatten_sensor_data(filepath):
    with open(filepath, "r") as f:
        lines = [json.loads(line) for line in f]
    return pd.json_normalize(lines)

def plot_dashboard(df):
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("🔧 Sensor System Monitoring Dashboard", fontsize=18, fontweight="bold")

    # 1️⃣ Battery Temperature Distribution
    sns.histplot(df["battery.temperature"], kde=True, ax=axs[0, 0], bins=30, color="#FF7F0E")
    axs[0, 0].set_title("Battery Temperature Distribution")
    axs[0, 0].set_xlabel("Temperature (°C)")

    # 2️⃣ Vibration Levels
    sns.boxplot(y=df["motor.vibration_level"], ax=axs[0, 1], color="#2CA02C")
    axs[0, 1].set_title("Motor Vibration Level")
    axs[0, 1].set_ylabel("Vibration Intensity")

    # 3️⃣ Error Code Frequency
    error_counts = df["battery.error_code"].value_counts().reset_index()
    error_counts.columns = ['error_code', 'count']

    sns.barplot(x="error_code", y="count", data=error_counts, ax=axs[1, 0], palette="flare")
    axs[1, 0].set_title("Battery Error Code Frequency")
    axs[1, 0].set_xlabel("Error Code")
    axs[1, 0].set_ylabel("Count")

    # 4️⃣ Anomalies Over Time (High temp + vibration)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["anomaly"] = ((df["battery.temperature"] > 80) & (df["motor.vibration_level"] > 1.0)).astype(int)
    anomalies = df.set_index("timestamp").resample("1min")["anomaly"].sum()
    anomalies.plot(ax=axs[1, 1], color="red", linewidth=2)
    axs[1, 1].set_title("Anomalies Over Time")
    axs[1, 1].set_ylabel("Anomalies per Minute")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    df = load_and_flatten_sensor_data("data/sensor_data_stream.jsonl")
    plot_dashboard(df)
