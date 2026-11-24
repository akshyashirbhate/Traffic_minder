
import pandas as pd

from app.ml.model_loader import xgboost_model


FEATURE_COLUMNS = [
    "speed",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "rolling_mean_6",
    "hour",
    "minute",
    "day_of_week"
]


def get_traffic_status(speed: float) -> str:
    if speed < 15:
        return "Heavy Traffic"
    elif speed < 30:
        return "Moderate Traffic"
    else:
        return "Free Flow"


def predict_traffic(data):
    # Convert validated request into a dictionary
    input_data = data.model_dump()

    # Prepare input in the exact order required by XGBoost
    input_df = pd.DataFrame(
        [[input_data[column] for column in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    # Predict the speed for the next 5-minute interval
    prediction = xgboost_model.predict(input_df)[0]

    # Keep prediction within reasonable speed limits
    prediction = max(0.0, min(150.0, float(prediction)))

    # Determine traffic condition
    traffic_status = get_traffic_status(prediction)

    return {
        "current_speed": round(float(input_data["speed"]), 2),
        "predicted_speed": round(prediction, 2),
        "prediction_interval": "Next 5 minutes",
        "traffic_status": traffic_status,
        "model": "XGBoost"
    }
