from fastapi import APIRouter
from api.models.schemas import SensorInput, PredictionOutput
from api.utils.processor import predict_failure

router = APIRouter()

@router.post("/", response_model=PredictionOutput)
def predict_failure_endpoint(sensor_data: SensorInput):
    return predict_failure(sensor_data)
