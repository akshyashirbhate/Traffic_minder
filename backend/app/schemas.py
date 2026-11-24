from pydantic import BaseModel, Field


class TrafficPredictionRequest(BaseModel):
    speed: float = Field(..., ge=0, le=150)
    lag_1: float = Field(..., ge=0, le=150)
    lag_2: float = Field(..., ge=0, le=150)
    lag_3: float = Field(..., ge=0, le=150)

    rolling_mean_3: float = Field(..., ge=0, le=150)
    rolling_mean_6: float = Field(..., ge=0, le=150)

    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    day_of_week: int = Field(..., ge=0, le=6)

class TrafficPatternRequest(BaseModel):
    speed: float = Field(..., ge=0, le=150)
    lag_1: float = Field(..., ge=0, le=150)
    lag_2: float = Field(..., ge=0, le=150)
    lag_3: float = Field(..., ge=0, le=150)
    rolling_mean_3: float = Field(..., ge=0, le=150)
    rolling_mean_6: float = Field(..., ge=0, le=150)