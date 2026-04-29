import csv
import json
import os

from acquiring_data.distance_requests import CSV_PATH, get_distances

OUTPUT_DIR = os.path.join("data", "all_data")


def pull_batch(batch: int) -> None:
    if not 0 <= batch <= 4:
        raise ValueError("batch must be an int 0-4")

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        towns = [row[0].strip().strip('"') for row in reader if any(row)]

    batch_towns = towns[batch * 20 : (batch + 1) * 20]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for city in batch_towns:
        for modality in ("driving", "bicycling"):
            try:
                data = get_distances(city, modality)
            except Exception as e:
                print(f"ERROR {city} [{modality}]: {e}")
                continue

            # JSON requires string keys, so serialize tuple keys as "origin|destination"
            serializable = {
                f"{origin}|{dest}": value
                for (origin, dest), value in data.items()
            }

            safe_name = city.replace(", ", "_").replace(" ", "_")
            filename = os.path.join(OUTPUT_DIR, f"{safe_name}_{modality}.json")

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    {"city": city, "modality": modality, "distances": serializable},
                    f,
                    indent=2,
                )
            print(f"Wrote {filename}")