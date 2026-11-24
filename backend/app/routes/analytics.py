
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.database import get_db
from app.models import TrafficAnalysis


router = APIRouter(
    prefix="/api/traffic",
    tags=["Traffic Analytics"]
)


# ==========================================
# 1. Traffic Analytics Summary
# ==========================================
@router.get("/analytics")
def get_traffic_analytics(db: Session = Depends(get_db)):

    total_analyses = db.query(TrafficAnalysis).count()

    average_current_speed = db.query(
        func.avg(TrafficAnalysis.current_speed)
    ).scalar()

    average_predicted_speed = db.query(
        func.avg(TrafficAnalysis.predicted_speed)
    ).scalar()

    maximum_speed = db.query(
        func.max(TrafficAnalysis.current_speed)
    ).scalar()

    minimum_speed = db.query(
        func.min(TrafficAnalysis.current_speed)
    ).scalar()

    anomalies_detected = db.query(TrafficAnalysis).filter(
        TrafficAnalysis.is_anomaly == True
    ).count()

    normal_observations = total_analyses - anomalies_detected

    anomaly_percentage = (
        (anomalies_detected / total_analyses) * 100
        if total_analyses > 0 else 0
    )

    traffic_distribution = (
        db.query(
            TrafficAnalysis.traffic_status,
            func.count(TrafficAnalysis.id)
        )
        .group_by(TrafficAnalysis.traffic_status)
        .all()
    )

    distribution = {}

    for status, count in traffic_distribution:

        percentage = (
            (count / total_analyses) * 100
            if total_analyses > 0 else 0
        )

        distribution[status] = {
            "count": count,
            "percentage": round(percentage, 2)
        }

    return {
        "total_analyses": total_analyses,

        "speed_statistics": {
            "average_current_speed": round(average_current_speed, 2)
            if average_current_speed is not None else 0,

            "average_predicted_speed": round(average_predicted_speed, 2)
            if average_predicted_speed is not None else 0,

            "maximum_speed": maximum_speed,
            "minimum_speed": minimum_speed
        },

        "anomaly_statistics": {
            "anomalies_detected": anomalies_detected,
            "normal_observations": normal_observations,
            "anomaly_percentage": round(anomaly_percentage, 2)
        },

        "traffic_distribution": distribution,

        "status": "success"
    }


# ==========================================
# 2. Historical Traffic Trends
# ==========================================
@router.get("/trends")
def get_traffic_trends(
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db)
):

    records = (
        db.query(TrafficAnalysis)
        .order_by(TrafficAnalysis.created_at.desc())
        .limit(limit)
        .all()
    )

    # Reverse records to chronological order
    records.reverse()

    trends = []

    for record in records:

        trends.append({
            "id": record.id,
            "current_speed": record.current_speed,
            "predicted_speed": record.predicted_speed,
            "traffic_status": record.traffic_status,
            "cluster_id": record.cluster_id,
            "cluster_name": record.cluster_name,
            "is_anomaly": record.is_anomaly,
            "anomaly_score": record.anomaly_score,
            "timestamp": (
                record.created_at.isoformat()
                if record.created_at else None
            )
        })

    return {
        "total_records": len(trends),
        "trends": trends,
        "status": "success"
    }


# ==========================================
# 3. Peak-Hour Traffic Analytics
# ==========================================
@router.get("/peak-hours")
def get_peak_hour_analytics(db: Session = Depends(get_db)):

    # Extract hour from timestamp (SQLite)
    hour_expression = func.strftime(
        "%H",
        TrafficAnalysis.created_at
    )

    # Aggregate traffic data by hour
    hourly_records = (
        db.query(
            hour_expression.label("hour"),

            func.count(TrafficAnalysis.id).label("total_analyses"),

            func.avg(
                TrafficAnalysis.current_speed
            ).label("average_speed"),

            func.sum(
                case(
                    (TrafficAnalysis.traffic_status == "Heavy Traffic", 1),
                    else_=0
                )
            ).label("heavy_traffic_count"),

            func.sum(
                case(
                    (TrafficAnalysis.traffic_status == "Moderate Traffic", 1),
                    else_=0
                )
            ).label("moderate_traffic_count"),

            func.sum(
                case(
                    (TrafficAnalysis.traffic_status == "Free Flow", 1),
                    else_=0
                )
            ).label("free_flow_count")

        )
        .group_by(hour_expression)
        .order_by(hour_expression)
        .all()
    )

    hourly_traffic = []

    for record in hourly_records:

        hourly_traffic.append({
            "hour": int(record.hour),
            "time_range": f"{int(record.hour):02d}:00 - {int(record.hour):02d}:59",
            "total_analyses": record.total_analyses,
            "average_speed": round(record.average_speed, 2)
            if record.average_speed is not None else 0,
            "heavy_traffic_count": record.heavy_traffic_count,
            "moderate_traffic_count": record.moderate_traffic_count,
            "free_flow_count": record.free_flow_count
        })

    # Find hour with the highest heavy traffic count
    peak_hour = None

    if hourly_traffic:

        peak_hour = max(
            hourly_traffic,
            key=lambda item: item["heavy_traffic_count"]
        )

    return {
        "total_records": sum(
            record["total_analyses"]
            for record in hourly_traffic
        ),

        "peak_congestion_hour": (
            peak_hour["time_range"]
            if peak_hour and peak_hour["heavy_traffic_count"] > 0
            else None
        ),

        "peak_hour_details": peak_hour,

        "hourly_traffic": hourly_traffic,

        "status": "success"
    }
