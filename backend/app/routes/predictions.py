
from fastapi import APIRouter

from app.schemas import (
    TrafficPredictionRequest,
    TrafficPatternRequest
)

from app.services.prediction_service import predict_traffic
from app.services.traffic_service import detect_traffic_pattern


router = APIRouter(
    prefix="/api/traffic",
    tags=["Traffic AI"]
)


# XGBoost - Predict traffic speed for next 5 minutes
@router.post("/predict")
def traffic_prediction(request: TrafficPredictionRequest):
    return predict_traffic(request)


# K-Means - Detect traffic pattern
@router.post("/pattern")
def traffic_pattern(request: TrafficPatternRequest):
    return detect_traffic_pattern(request)
