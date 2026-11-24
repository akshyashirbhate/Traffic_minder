from sqlalchemy.orm import Session

from app.models import LiveTrafficObservation
from app.services.tomtom_service import get_live_traffic


def collect_live_traffic(
    latitude: float,
    longitude: float,
    db: Session
):
    # Step 1: Fetch live traffic data from TomTom
    traffic_data = get_live_traffic(latitude, longitude)

    # Step 2: Create a database record
    observation = LiveTrafficObservation(
        latitude=latitude,
        longitude=longitude,
        current_speed=traffic_data.get("current_speed"),
        free_flow_speed=traffic_data.get("free_flow_speed"),
        current_travel_time=traffic_data.get("current_travel_time"),
        free_flow_travel_time=traffic_data.get("free_flow_travel_time"),
        confidence=traffic_data.get("confidence"),
        road_closure=traffic_data.get("road_closure")
    )

    # Step 3: Save observation to database
    db.add(observation)
    db.commit()
    db.refresh(observation)

    # Step 4: Return saved observation
    return {
        "observation_id": observation.id,
        "latitude": observation.latitude,
        "longitude": observation.longitude,
        "current_speed": observation.current_speed,
        "free_flow_speed": observation.free_flow_speed,
        "current_travel_time": observation.current_travel_time,
        "free_flow_travel_time": observation.free_flow_travel_time,
        "confidence": observation.confidence,
        "road_closure": observation.road_closure,
        "observed_at": observation.observed_at,
        "data_source": "TomTom Traffic API",
        "message": "Live traffic observation saved successfully"
    }