# api/routes/recommend.py
from fastapi import APIRouter
from api.models.schemas import SensorInput, MaintenanceDecision
from api.utils.processor import recommend_maintenance

router = APIRouter()

@router.post("/recommend-maintenance", response_model=MaintenanceDecision)
def recommend(sensor_data: SensorInput):
    return recommend_maintenance(sensor_data)
