
import joblib
from pathlib import Path
from xgboost import XGBRegressor

# =====================================================
# MODEL DIRECTORY
# =====================================================

MODEL_DIR = Path(__file__).resolve().parents[2] / "models"

print(f"\nLoading Traffic Minder models from: {MODEL_DIR}\n")

# =====================================================
# 1. XGBOOST MODEL (JSON)
# =====================================================

xgboost_model = XGBRegressor()

xgboost_model.load_model(
    str(MODEL_DIR / "xgboost_traffic_model.json")
)

print("[OK] XGBoost model loaded")

# =====================================================
# 2. K-MEANS MODEL
# =====================================================

kmeans_model = joblib.load(
    MODEL_DIR / "kmeans_traffic_model.joblib"
)

kmeans_scaler = joblib.load(
    MODEL_DIR / "kmeans_scaler.joblib"
)

print("[OK] K-Means model loaded")
print("[OK] K-Means scaler loaded")

# =====================================================
# 3. ISOLATION FOREST MODEL
# =====================================================

isolation_forest_model = joblib.load(
    MODEL_DIR / "isolation_forest_model.joblib"
)

isolation_forest_scaler = joblib.load(
    MODEL_DIR / "isolation_forest_scaler.joblib"
)

print("[OK] Isolation Forest model loaded")
print("[OK] Isolation Forest scaler loaded")

# =====================================================
# 4. SUCCESS
# =====================================================

print("\n====================================")
print("ALL TRAFFIC MINDER MODELS LOADED")
print("====================================\n")
