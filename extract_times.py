import csv
import json
import os

DATA_DIR = os.path.join("data", "all_data")
OUTPUT_DIR = os.path.join("data", "travel_time_data")

ORIGINS = ["home", "local icon", "grocery", "hospital", "stadium"]
DESTINATIONS = ["home", "downtown", "nature", "nearby city"]


def extract_times() -> None:
    """
    For each JSON file in DATA_DIR, writes a CSV of duration_s values
    with origins as rows and destinations as columns.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        distances = data["distances"]

        stem = os.path.splitext(filename)[0]
        out_path = os.path.join(OUTPUT_DIR, f"{stem}_times.csv")

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([""] + DESTINATIONS)
            for origin in ORIGINS:
                row = [origin]
                for dest in DESTINATIONS:
                    key = f"{origin}|{dest}"
                    entry = distances.get(key)
                    if entry and "duration_s" in entry:
                        row.append(entry["duration_s"])
                    else:
                        row.append("")
                writer.writerow(row)

        print(f"Wrote {out_path}")


if __name__ == "__main__":
    extract_times()
