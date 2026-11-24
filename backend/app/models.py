from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class TrafficAnalysis(Base):

    __tablename__ = "traffic_analysis"

    id = Column(Integer, primary_key=True, index=True)

    current_speed = Column(Float, nullable=False)
    predicted_speed = Column(Float, nullable=True)

    cluster_id = Column(Integer, nullable=True)
    cluster_name = Column(String, nullable=True)

    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float, nullable=True)

    traffic_status = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


# NEW MODEL: Stores live traffic observations from TomTom
class LiveTrafficObservation(Base):

    __tablename__ = "live_traffic_observations"

    id = Column(Integer, primary_key=True, index=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    current_speed = Column(Float, nullable=False)
    free_flow_speed = Column(Float, nullable=True)

    current_travel_time = Column(Integer, nullable=True)
    free_flow_travel_time = Column(Integer, nullable=True)

    confidence = Column(Float, nullable=True)
    road_closure = Column(Boolean, nullable=True)

    observed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )