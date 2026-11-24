from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.predictions import router as predictions_router
from app.routes.anomalies import router as anomalies_router
from app.routes.traffic import router as traffic_router
from app.routes.analytics import router as analytics_router

from app.database import Base, engine
from app import models

from app.services.traffic_scheduler import (
    start_traffic_scheduler,
    stop_traffic_scheduler
)


# Application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize database tables
    Base.metadata.create_all(bind=engine)

    # Start automated traffic analysis scheduler
    start_traffic_scheduler()

    print("====================================")
    print("TRAFFIC MINDER BACKEND STARTED")
    print("AUTOMATED TRAFFIC ANALYSIS ENABLED")
    print("ANALYSIS INTERVAL: 5 MINUTES")
    print("====================================")

    yield

    # Stop scheduler during application shutdown
    stop_traffic_scheduler()

    print("Traffic Minder backend stopped.")


# Initialize FastAPI application
app = FastAPI(
    title="Traffic Minder API",
    description="AI-powered traffic prediction and anomaly detection backend",
    version="1.0.0",
    lifespan=lifespan
)


# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(predictions_router)
app.include_router(anomalies_router)
app.include_router(traffic_router)
app.include_router(analytics_router)


# Home endpoint
@app.get("/")
def home():
    return {
        "project": "Traffic Minder",
        "message": "Traffic Minder API is running",
        "status": "active"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Traffic Minder Backend"
    }