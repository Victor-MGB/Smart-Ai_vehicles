import seaborn as sns
import matplotlib.pyplot as plt

def plot_decision_breakdown(df_decisions):
    sns.set(style="whitegrid", font_scale=1.1)
    
    # Count decisions
    decision_counts = df_decisions['decision'].value_counts().reset_index()
    decision_counts.columns = ['Decision', 'Count']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Decision', y='Count', data=decision_counts, palette='viridis')
    
    plt.title("Decision Breakdown: FIX vs WAIT", fontsize=16, weight='bold')
    plt.xlabel("Decision")
    plt.ylabel("Number of Components")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()