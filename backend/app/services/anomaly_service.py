from app.ml.model_loader import (
    isolation_forest_model,
    isolation_forest_scaler
)

FEATURE_COLUMNS = [
    "speed",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "rolling_mean_6"
]


def detect_traffic_anomaly(data):

    input_data = data.model_dump()

    # Prepare the six input features
    features = [
        input_data[column]
        for column in FEATURE_COLUMNS
    ]

    # Scale input using the scaler used during training
    scaled_data = isolation_forest_scaler.transform([features])

    # Detect normal or anomalous traffic
    prediction = isolation_forest_model.predict(scaled_data)[0]

    # Get anomaly score
    anomaly_score = isolation_forest_model.decision_function(scaled_data)[0]

    # -1 means anomaly, 1 means normal
    if prediction == -1:
        status = "Anomaly Detected"
        is_anomaly = True
    else:
        status = "Normal Traffic"
        is_anomaly = False

    return {
        "current_speed": input_data["speed"],
        "is_anomaly": is_anomaly,
        "traffic_status": status,
        "anomaly_score": round(float(anomaly_score), 4),
        "model": "Isolation Forest",
        "status": "success"
    }