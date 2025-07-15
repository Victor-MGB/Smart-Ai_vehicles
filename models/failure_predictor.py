import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import logging
import joblib

logging.basicConfig(level=logging.INFO)

def train_failure_model(sensor_df: pd.DataFrame) -> Pipeline:
    """
    Trains a logistic regression model to predict component failure based on sensor data.
    Returns the trained pipeline.
    """
    # Validate input columns
    required_cols = ['battery.temperature', 'motor.vibration_level', 'battery.error_code']
    for col in required_cols:
        if col not in sensor_df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Create label
    sensor_df['error_flag'] = sensor_df['battery.error_code'].apply(lambda x: 1 if x != 'OK' else 0)
    sensor_df['failure'] = ((sensor_df['battery.temperature'] > 85) & 
                            (sensor_df['motor.vibration_level'] > 1.0)) | (sensor_df['error_flag'] == 1)
    sensor_df['failure'] = sensor_df['failure'].astype(int)

    X = sensor_df[['battery.temperature', 'motor.vibration_level', 'error_flag']]
    y = sensor_df['failure']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=200))
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    logging.info("\n📋 Classification Report:\n%s", classification_report(y_test, y_pred))

    # Optionally save the model
    joblib.dump(model, "model/failure_predictor.pkl")

    return model

def predict_failure_probabilities(model: Pipeline, sensor_df: pd.DataFrame) -> pd.DataFrame:
    """
    Predicts failure probabilities for each component using the trained model.
    """
    sensor_df = sensor_df.copy()  # Avoid modifying original
    sensor_df['error_flag'] = sensor_df['battery.error_code'].apply(lambda x: 1 if x != 'OK' else 0)

    features = sensor_df[['battery.temperature', 'motor.vibration_level', 'error_flag']]
    probabilities = model.predict_proba(features)[:, 1]

    sensor_df['failure_probability'] = probabilities
    return sensor_df[['component_id', 'vehicle_id', 'failure_probability']]
