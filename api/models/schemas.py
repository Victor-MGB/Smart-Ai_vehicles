# api/models/schemas.py
from pydantic import BaseModel
from typing import Optional

class Battery(BaseModel):
    temperature: float
    voltage: float
    error_code: str

class Motor(BaseModel):
    vibration_level: float
    torque: float
    error_code: str

class BrakeSystem(BaseModel):
    brake_pad_thickness: float
    temperature: float
    error_code: str

class Location(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]

class SensorInput(BaseModel):
    component_id: str
    vehicle_id: str
    timestamp: str
    location: Optional[Location]
    battery: Battery
    motor: Motor
    brake_system: BrakeSystem
    last_service_date: str
    component_age_days: int

class MaintenanceDecision(BaseModel):
    component_id: str
    vehicle_id: str
    failure_probability: float
    recommended_action: str
    explanation: str
    
class PredictionOutput(BaseModel):
    component_id: str
    vehicle_id: str
    failure_probability: float