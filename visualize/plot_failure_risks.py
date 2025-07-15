# visualize/plot_failure_risks.py

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_failure_probabilities(df_with_probs: pd.DataFrame):
    sns.set(style="whitegrid", font_scale=1.1)
    df_sorted = df_with_probs.sort_values(by='failure_probability', ascending=False).reset_index(drop=True)
    df_sorted['component_idx'] = df_sorted.index + 1

    plt.figure(figsize=(14, 6))
    sns.lineplot(x='component_idx', y='failure_probability', data=df_sorted, marker='o', linewidth=2, color='crimson')

    high_risk = df_sorted[df_sorted['failure_probability'] > 0.75]
    plt.scatter(high_risk['component_idx'], high_risk['failure_probability'], color='red', label='High Risk 🔥', zorder=5)

    plt.title("📉 Predicted Failure Probability per Component", fontsize=16, weight='bold')
    plt.xlabel("Component Index (sorted by risk)")
    plt.ylabel("Failure Probability")
    plt.axhline(0.75, linestyle='--', color='gray', label="Risk Threshold = 0.75")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()
