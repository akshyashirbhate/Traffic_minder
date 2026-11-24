
from app.ml.model_loader import kmeans_model, kmeans_scaler


FEATURE_COLUMNS = [
    "speed",
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "rolling_mean_6"
]


def detect_traffic_pattern(data):
    # Convert request to dictionary
    input_data = data.model_dump()

    # Arrange features in the exact training order
    features = [
        input_data[column]
        for column in FEATURE_COLUMNS
    ]

    # Scale input using the original training scaler
    scaled_data = kmeans_scaler.transform([features])

    # Predict cluster
    cluster_id = int(kmeans_model.predict(scaled_data)[0])

    return {
        "cluster_id": cluster_id,
        "cluster_name": f"Traffic Cluster {cluster_id}",
        "current_speed": input_data["speed"],
        "model": "K-Means",
        "status": "success"
    }
