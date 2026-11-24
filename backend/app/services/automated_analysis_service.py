from sqlalchemy.orm import Session

from app.schemas import TrafficPredictionRequest

from app.services.live_traffic_service import collect_live_traffic
from app.services.feature_engineering_service import generate_traffic_features
from app.services.analysis_service import analyze_traffic


def run_automated_traffic_analysis(
    latitude: float,
    longitude: float,
    db: Session
):
    """
    Automated traffic analysis pipeline.

    Flow:
    1. Collect live traffic from TomTom.
    2. Store the observation.
    3. Generate features from historical traffic.
    4. Validate features.
    5. Run all 3 ML models.
    6. Save combined analysis.
    """

    # Step 1: Fetch live traffic and save observation
    live_data = collect_live_traffic(
        latitude=latitude,
        longitude=longitude,
        db=db
    )

    # Step 2: Generate ML features from historical observations
    feature_result = generate_traffic_features(
        latitude=latitude,
        longitude=longitude,
        db=db
    )

    # Step 3: Check whether feature generation succeeded
    if feature_result["status"] != "success":
        return {
            "status": "insufficient_data",
            "message": "Traffic data collected, but insufficient historical observations for ML analysis.",
            "live_traffic": live_data,
            "feature_result": feature_result
        }

    # Step 4: Extract generated features
    features = feature_result["features"]

    # Step 5: Validate features using Pydantic schema
    prediction_request = TrafficPredictionRequest(**features)

    # Step 6: Run the complete 3-model analysis
    analysis_result = analyze_traffic(
        data=prediction_request,
        db=db
    )

    # Step 7: Return the complete automated result
    return {
        "status": "success",
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "live_traffic": live_data,
        "feature_engineering": {
            "observation_count": feature_result["observation_count"],
            "latest_observation": feature_result["latest_observation"],
            "features": features
        },
        "traffic_analysis": analysis_result,
        "pipeline": [
            "TomTom Live Traffic Collection",
            "Historical Data Storage",
            "Feature Engineering",
            "XGBoost Speed Prediction",
            "K-Means Traffic Pattern Detection",
            "Isolation Forest Anomaly Detection",
            "Database Storage"
        ]
    }