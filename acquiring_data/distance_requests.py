# code to get distance between two locations using Google Maps API

import csv
import requests

API_KEY = "AIzaSyBEt3eMxLSFSm2maeJNld8j776jy8z7cBw"
CSV_PATH = "townNamesLatLong.csv"

COLUMN_INDEX = {
    "home": 1,
    "downtown": 2,
    "nature": 3,
    "local icon": 4,
    "grocery": 5,
    "hospital": 6,
    "stadium": 7,
    "nearby city": 8,
}

origins = ["home", "local icon", "grocery", "hospital", "stadium"]
destinations = ["home", "downtown", "nature", "nearby city"]


def get_distances(city_name: str, modality: str) -> dict:
    """
    Returns a distance matrix from the Google Maps Distance Matrix API
    for all origin/destination pairs for the given city.

    modality: "driving" or "bicycling"
    Returns: dict with keys (origin, destination) -> {"distance": ..., "duration": ...}
    """
    if modality not in ("driving", "bicycling"):
        raise ValueError("modality must be 'driving' or 'bicycling'")

    # Load city coordinates from CSV
    city_coords = None
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row[0].strip().strip('"') == city_name:
                city_coords = row
                break

    if city_coords is None:
        raise ValueError(f"City '{city_name}' not found in {CSV_PATH}")

    def get_latlong(label: str) -> str:
        coord = city_coords[COLUMN_INDEX[label]].strip().strip('"')
        if not coord:
            raise ValueError(f"No coordinates for '{label}' in city '{city_name}'")
        return coord

    origin_coords = [get_latlong(o) for o in origins]
    destination_coords = [get_latlong(d) for d in destinations]

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(origin_coords),
        "destinations": "|".join(destination_coords),
        "mode": modality,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data["status"] != "OK":
        raise RuntimeError(f"API error: {data['status']}")

    results = {}
    for i, origin_label in enumerate(origins):
        row = data["rows"][i]["elements"]
        for j, dest_label in enumerate(destinations):
            element = row[j]
            if element["status"] == "OK":
                results[(origin_label, dest_label)] = {
                    "distance_m": element["distance"]["value"],
                    "distance_text": element["distance"]["text"],
                    "duration_s": element["duration"]["value"],
                    "duration_text": element["duration"]["text"],
                }
            else:
                results[(origin_label, dest_label)] = {"status": element["status"]}

    return results
