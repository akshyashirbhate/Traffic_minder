import logging

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.automated_analysis_service import run_automated_traffic_analysis


# Configure logging
logger = logging.getLogger(__name__)


# Los Angeles (Downtown / US-101 highway corridor)
LATITUDE = 19.0596 
LONGITUDE = 72.8295


def automated_traffic_job():
    """
    Automatically run the complete traffic analysis pipeline.

    Pipeline:
    1. Collect live traffic from TomTom
    2. Save traffic observation
    3. Generate ML features
    4. Run XGBoost prediction
    5. Run K-Means classification
    6. Run Isolation Forest anomaly detection
    7. Save analysis to database
    """

    db: Session = SessionLocal()

    try:
        result = run_automated_traffic_analysis(
            latitude=LATITUDE,
            longitude=LONGITUDE,
            db=db
        )

        if result.get("status") == "success":

            traffic_analysis = result.get("traffic_analysis", {})

            logger.info(
                "Automated traffic analysis completed successfully. "
                "Current Speed: %s km/h | Predicted Speed: %s km/h | Status: %s",
                traffic_analysis.get("current_speed"),
                traffic_analysis.get("predicted_speed"),
                traffic_analysis.get("traffic_status")
            )

        else:
            logger.warning(
                "Automated traffic analysis completed with status: %s",
                result.get("status")
            )

    except Exception as e:

        logger.exception(
            "Automated traffic analysis failed: %s",
            str(e)
        )

    finally:
        db.close()


# Create scheduler
scheduler = BackgroundScheduler()


def start_traffic_scheduler():
    """
    Start automatic traffic analysis every 5 minutes.
    """

    if scheduler.running:
        logger.info("Traffic scheduler is already running.")
        return

    scheduler.add_job(
        automated_traffic_job,
        trigger="interval",
        minutes=5,
        id="automated_traffic_analysis",
        replace_existing=True,
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

    logger.info(
        "Automated traffic scheduler started. "
        "Full ML analysis interval: 5 minutes."
    )


def stop_traffic_scheduler():
    """
    Stop the scheduler.
    """

    if scheduler.running:
        scheduler.shutdown(wait=False)

        logger.info(
            "Automated traffic scheduler stopped."
        )