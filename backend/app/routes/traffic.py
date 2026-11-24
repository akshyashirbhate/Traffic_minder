from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import TrafficPredictionRequest
from app.database import get_db
from app.models import TrafficAnalysis

from app.services.analysis_service import analyze_traffic
from app.services.tomtom_service import get_live_traffic
from app.services.live_traffic_service import collect_live_traffic
from app.services.historical_traffic_service import get_historical_traffic
from app.services.feature_engineering_service import generate_traffic_features
from app.services.automated_analysis_service import run_automated_traffic_analysis


router = APIRouter(
    prefix="/api/traffic",
    tags=["Traffic Analysis"]
)


# ==========================================
# 1. Combined Analysis of All 3 ML Models
# ==========================================
@router.post("/analyze")
def traffic_analysis(
    request: TrafficPredictionRequest,
    db: Session = Depends(get_db)
):
    return analyze_traffic(request, db)


# ==========================================
# 2. Retrieve Traffic Analysis History
# ==========================================
@router.get("/history")
def get_traffic_history(
    db: Session = Depends(get_db)
):
    records = (
        db.query(TrafficAnalysis)
        .order_by(TrafficAnalysis.id.desc())
        .all()
    )

    return {
        "total_records": len(records),
        "history": [
            {
                "id": record.id,
                "current_speed": record.current_speed,
                "predicted_speed": record.predicted_speed,
                "cluster_id": record.cluster_id,
                "cluster_name": record.cluster_name,
                "is_anomaly": record.is_anomaly,
                "anomaly_score": record.anomaly_score,
                "traffic_status": record.traffic_status,
                "created_at": (
                    record.created_at.isoformat()
                    if record.created_at else None
                )
            }
            for record in records
        ]
    }


# ==========================================
# 3. Fetch Live Traffic Data from TomTom
# ==========================================
@router.get("/live")
def live_traffic(
    latitude: float,
    longitude: float
):
    return get_live_traffic(latitude, longitude)


# ==========================================
# 4. Fetch Live Traffic and Save to Database
# ==========================================
@router.post("/live/collect")
def collect_traffic_data(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):
    return collect_live_traffic(
        latitude=latitude,
        longitude=longitude,
        db=db
    )


# ==========================================
# 5. Retrieve Historical Traffic Observations
# ==========================================
@router.get("/historical")
def historical_traffic(
    latitude: float,
    longitude: float,
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_historical_traffic(
        latitude=latitude,
        longitude=longitude,
        db=db,
        limit=limit
    )


# ==========================================
# 6. Generate ML Features from Historical Data
# ==========================================
@router.get("/features")
def traffic_features(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):
    return generate_traffic_features(
        latitude=latitude,
        longitude=longitude,
        db=db
    )


# ==========================================
# 7. Automated Traffic Analysis Pipeline
# ==========================================
@router.post("/automated-analyze")
def automated_traffic_analysis(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):
    return run_automated_traffic_analysis(
        latitude=latitude,
        longitude=longitude,
        db=db
    )