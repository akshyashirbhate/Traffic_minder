from sqlalchemy.orm import Session

from app.models import LiveTrafficObservation


def generate_traffic_features(
    latitude: float,
    longitude: float,
    db: Session
):
    """
    Generate ML features from historical traffic observations.
    """

    # Fetch the latest 6 observations for the requested location
    records = (
        db.query(LiveTrafficObservation)
        .filter(
            LiveTrafficObservation.latitude == latitude,
            LiveTrafficObservation.longitude == longitude
        )
        .order_by(LiveTrafficObservation.id.desc())
        .limit(6)
        .all()
    )

    # Reverse to get chronological order (oldest -> newest)
    records.reverse()

    # Require at least 6 observations
    if len(records) < 6:
        return {
            "status": "insufficient_data",
            "message": "At least 6 traffic observations are required.",
            "available_records": len(records),
            "required_records": 6
        }

    # Extract speeds
    speeds = [record.current_speed for record in records]

    # Current and previous speeds
    current_speed = speeds[-1]
    lag_1 = speeds[-2]
    lag_2 = speeds[-3]
    lag_3 = speeds[-4]

    # Rolling averages
    rolling_mean_3 = sum(speeds[-3:]) / 3
    rolling_mean_6 = sum(speeds[-6:]) / 6

    # Latest observation timestamp
    latest_record = records[-1]
    observed_at = latest_record.observed_at

    # Time-based features
    hour = observed_at.hour
    minute = observed_at.minute
    day_of_week = observed_at.weekday()

    # Prepare ML feature dictionary
    features = {
        "speed": current_speed,
        "lag_1": lag_1,
        "lag_2": lag_2,
        "lag_3": lag_3,
        "rolling_mean_3": rolling_mean_3,
        "rolling_mean_6": rolling_mean_6,
        "hour": hour,
        "minute": minute,
        "day_of_week": day_of_week
    }

    return {
        "status": "success",
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "observation_count": len(records),
        "latest_observation": observed_at.isoformat() if observed_at else None,
        "features": features
    }