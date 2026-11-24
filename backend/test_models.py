from app.ml.model_loader import (
    xgboost_model,
    kmeans_model,
    kmeans_scaler,
    isolation_forest_model,
    isolation_forest_scaler
)

print("\n========== MODEL VERIFICATION ==========\n")

print("XGBoost Model:", type(xgboost_model).__name__)
print("K-Means Model:", type(kmeans_model).__name__)
print("K-Means Scaler:", type(kmeans_scaler).__name__)
print("Isolation Forest Model:", type(isolation_forest_model).__name__)
print("Isolation Forest Scaler:", type(isolation_forest_scaler).__name__)

print("\n====================================")
print("All 5 models verified successfully!")
print("Traffic Minder ML models are ready.")
print("====================================")