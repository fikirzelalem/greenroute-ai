# cuopt.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_real_routes(start, end):
    """
    Fetches real routes between two points using Google Maps Directions API.
    """
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "alternatives": "true",
        "key": GOOGLE_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    routes = []
    if data.get("routes"):
        for route in data["routes"]:
            leg = route["legs"][0]
            route_info = {
                "route": leg["start_address"] + " → " + leg["end_address"],
                "distance": round(leg["distance"]["value"] / 1000, 2),
                "time": round(leg["duration"]["value"] / 60, 1),
                "co2": round((leg["distance"]["value"] / 1000) * 0.12, 2),  # basic emission estimate
                "aqi": 50 + int(leg["duration"]["value"] / 300)  # mock AQI scaling
            }
            routes.append(route_info)

    return routes
