import pandas as pd
from models.failure_predictor import train_failure_model, predict_failure_probabilities
# run_failure_model.py
from models.failure_predictor import train_failure_model, predict_failure_probabilities
from visualize.plot_failure_risks import plot_failure_probabilities

# Load and flatten your data
df = pd.read_json("data/sensor_data_stream.jsonl", lines=True)
df_flat = pd.json_normalize(df.to_dict(orient="records"))

# Train model
model = train_failure_model(df_flat)

# Predict
predicted_df = predict_failure_probabilities(model, df_flat)

# Plot
plot_failure_probabilities(predicted_df)


def main():
    # Load simulated sensor data
    try:
        df = pd.read_json("data/sensor_data_stream.jsonl", lines=True)
    except Exception as e:
        print("❌ Failed to load data:", e)
        return

    df_flat = pd.json_normalize(df.to_dict(orient="records"))

    # Train model
    print("🚀 Training failure prediction model...")
    model = train_failure_model(df_flat)

    # Predict probabilities
    print("📊 Predicting failure probabilities...")
    predictions = predict_failure_probabilities(model, df_flat)

    # Show top risky components
    print(predictions.sort_values(by="failure_probability", ascending=False).head(10))

if __name__ == "__main__":
    main()
