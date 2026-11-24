from app.services.prediction_service import predict_traffic
from app.services.traffic_service import detect_traffic_pattern
from app.services.anomaly_service import detect_traffic_anomaly

from app.models import TrafficAnalysis


def analyze_traffic(data, db):

    # 1. XGBoost Prediction
    prediction_result = predict_traffic(data)

    # 2. K-Means Traffic Pattern
    pattern_result = detect_traffic_pattern(data)

    # 3. Isolation Forest Anomaly Detection
    anomaly_result = detect_traffic_anomaly(data)

    # 4. Save combined results into database
    analysis = TrafficAnalysis(
        current_speed=data.speed,
        predicted_speed=prediction_result["predicted_speed"],
        cluster_id=pattern_result["cluster_id"],
        cluster_name=pattern_result["cluster_name"],
        is_anomaly=anomaly_result["is_anomaly"],
        anomaly_score=anomaly_result["anomaly_score"],
        traffic_status=prediction_result["traffic_status"]
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # 5. Return combined response
    return {
        "analysis_id": analysis.id,
        "current_speed": analysis.current_speed,
        "predicted_speed": analysis.predicted_speed,
        "prediction_interval": prediction_result["prediction_interval"],
        "traffic_status": prediction_result["traffic_status"],
        "traffic_pattern": {
            "cluster_id": pattern_result["cluster_id"],
            "cluster_name": pattern_result["cluster_name"]
        },
        "anomaly_detection": {
            "is_anomaly": anomaly_result["is_anomaly"],
            "status": anomaly_result["traffic_status"],
            "anomaly_score": anomaly_result["anomaly_score"]
        },
        "models_used": [
            "XGBoost",
            "K-Means",
            "Isolation Forest"
        ],
        "database_status": "saved",
        "status": "success"
    }