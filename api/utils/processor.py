import pandas as pd
from typing import Dict
from api.models.schemas import SensorInput, MaintenanceDecision
from api.models.schemas import SensorInput

def predict_failure(sensor_data):
    """
    Process incoming sensor data and return a prediction result.

    Args:
        sensor_data (SensorInput): Incoming validated sensor data.

    Returns:
        dict: Prediction with failure probability and recommendation.
    """
    # Dummy logic for now – replace with your ML model
    prob = 0.8 if sensor_data.error_flag else 0.2
    recommended_action = "fix_now" if prob >= 0.6 else "wait"
    
    expected_cost_fix = 1000
    expected_cost_wait = int(prob * 5000)

    return {
        "component_id": sensor_data.component_id,
        "vehicle_id": getattr(sensor_data, "vehicle_id", "VH-1234"),
        "failure_probability": prob,
        "recommended_action": recommended_action,
        "expected_cost_fix": expected_cost_fix,
        "expected_cost_wait": expected_cost_wait,
        "explanation": f"Expected cost: {expected_cost_wait} > {expected_cost_fix}"
    }

# api/utils/processor.py

def recommend_maintenance(sensor_data: SensorInput):
    # Extract relevant fields
    battery_temp = sensor_data.battery.temperature
    motor_vibration = sensor_data.motor.vibration_level
    error_flag = 1 if sensor_data.battery.error_code != "OK" else 0

    # Your existing decision logic:
    # For example, failure_probability calculation, simple heuristic here:
    failure_probability = 0.0
    if battery_temp > 85 or motor_vibration > 1.0 or error_flag == 1:
        failure_probability = 0.9
    else:
        failure_probability = 0.1

    # Use your cost model here (example)
    cost_failure = 5000
    cost_fix = 1000
    threshold = 0.6

    expected_failure_cost = failure_probability * cost_failure
    recommended_action = "fix_now" if expected_failure_cost > cost_fix or failure_probability >= threshold else "wait"
    explanation = f"Expected failure cost {expected_failure_cost:.2f} vs fix cost {cost_fix}"

    return {
        "component_id": sensor_data.component_id,
        "vehicle_id": sensor_data.vehicle_id,
        "failure_probability": failure_probability,
        "recommended_action": recommended_action,
        "explanation": explanation
    }

