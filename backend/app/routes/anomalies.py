from fastapi import APIRouter

from app.schemas import TrafficPatternRequest
from app.services.anomaly_service import detect_traffic_anomaly

router = APIRouter(
    prefix="/api/traffic",
    tags=["Traffic Anomaly Detection"]
)


@router.post("/anomaly")
def traffic_anomaly(request: TrafficPatternRequest):
    return detect_traffic_anomaly(request)