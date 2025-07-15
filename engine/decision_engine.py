import pandas as pd

def recommend_action(prob, cost_failure, cost_fix, threshold=0.6):
    """
    Returns 'FIX' if expected cost of failure > early fix, else 'WAIT'.
    """
    
    expected_failure_cost = prob * cost_failure
    decision = "FIX" if expected_failure_cost > cost_fix or prob >= threshold else "WAIT"
    reason = f"Expected cost: {expected_failure_cost:.2f} > fix cost: {cost_fix}" if decision == "FIX" else "Below threshold"
    return decision, reason

def apply_decision_engine(sensor_df: pd.DataFrame, cost_config: dict):
    results = []
    for _, row in sensor_df.iterrows():
        comp_id = row['component_id']
        prob = row['failure_probability']
        cost_failure = cost_config.get('cost_failure', 5000)
        cost_fix = cost_config.get('early_fix_cost', 1000)
        
        decision, reason = recommend_action(prob, cost_failure, cost_fix)
        results.append({
            "component_id": comp_id,
            "vehicle_id": row['vehicle_id'],
            "failure_probability": prob,
            "decision": decision,
            "explanation": reason
        })

    return pd.DataFrame(results)