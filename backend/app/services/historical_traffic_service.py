
from sqlalchemy.orm import Session

from app.models import LiveTrafficObservation


def get_historical_traffic(
    latitude: float,
    longitude: float,
    db: Session,
    limit: int = 100
):
    """
    Retrieve the latest traffic observations for a location.

    Records are returned in chronological order
    (oldest to newest).
    """

    # Fetch the latest observations for the given location
    records = (
        db.query(LiveTrafficObservation)
        .filter(
            LiveTrafficObservation.latitude == latitude,
            LiveTrafficObservation.longitude == longitude
        )
        .order_by(LiveTrafficObservation.id.desc())
        .limit(limit)
        .all()
    )

    # Reverse to chronological order
    records.reverse()

    # Convert database records into JSON-friendly dictionaries
    history = [
        {
            "id": record.id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "current_speed": record.current_speed,
            "free_flow_speed": record.free_flow_speed,
            "current_travel_time": record.current_travel_time,
            "free_flow_travel_time": record.free_flow_travel_time,
            "confidence": record.confidence,
            "road_closure": record.road_closure,
            "observed_at": (
                record.observed_at.isoformat()
                if record.observed_at else None
            )
        }
        for record in records
    ]

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "total_records": len(history),
        "history": history
    }
