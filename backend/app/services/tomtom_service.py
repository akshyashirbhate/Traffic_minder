import os
import requests

from dotenv import load_dotenv

load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

TOMTOM_TRAFFIC_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"


def get_live_traffic(latitude: float, longitude: float):
    """
    Fetch live traffic information from TomTom for a given location.
    """

    if not TOMTOM_API_KEY:
        raise ValueError("TomTom API key not configured.")

    params = {
        "point": f"{latitude},{longitude}",
        "key": TOMTOM_API_KEY
    }

    response = requests.get(
        TOMTOM_TRAFFIC_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()
    flow = data.get("flowSegmentData", {})

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "current_speed": flow.get("currentSpeed"),
        "free_flow_speed": flow.get("freeFlowSpeed"),
        "current_travel_time": flow.get("currentTravelTime"),
        "free_flow_travel_time": flow.get("freeFlowTravelTime"),
        "confidence": flow.get("confidence"),
        "road_closure": flow.get("roadClosure"),
        "data_source": "TomTom Traffic API"
    }