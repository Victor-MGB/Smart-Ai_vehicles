import pandas as pd
import json
from models.failure_predictor import train_failure_model, predict_failure_probabilities
from engine.decision_engine import apply_decision_engine
from visualize.plot_fix_wait import plot_decision_breakdown

# Load and flatten
df = pd.read_json("data/sensor_data_stream.jsonl", lines=True)
df_flat = pd.json_normalize(df.to_dict(orient="records"))

# Train + Predict
model = train_failure_model(df_flat)
predicted = predict_failure_probabilities(model, df_flat)

# Load costs
with open("config/cost_model.json") as f:
    cost_cfg = json.load(f)

# Apply decision engine
decisions_df = apply_decision_engine(predicted, cost_cfg)

# Visualize
plot_decision_breakdown(decisions_df)

# Save output (optional)
decisions_df.to_csv("data/fix_wait_decisions.csv", index=False)
