import csv
import os
from modality_deltas import _read_time_csv

INPUT_DIR = os.path.join("data", "travel_time_data")
OUTPUT_DIR = os.path.join("data", "mod_delta_over_drive")


def compute_diff_over_drive() -> None:
    """
    For each city in INPUT_DIR, computes (t_bicycling - t_driving) / t_driving for every
    origin/destination pair and writes the result to OUTPUT_DIR as a CSV
    with the same row/column layout as the input files.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    bicycling_files = {
        f.replace("_bicycling_times.csv", "")
        for f in os.listdir(INPUT_DIR)
        if f.endswith("_bicycling_times.csv")
    }
    driving_files = {
        f.replace("_driving_times.csv", "")
        for f in os.listdir(INPUT_DIR)
        if f.endswith("_driving_times.csv")
    }
    cities = sorted(bicycling_files & driving_files)

    for city in cities:
        bike_path = os.path.join(INPUT_DIR, f"{city}_bicycling_times.csv")
        drive_path = os.path.join(INPUT_DIR, f"{city}_driving_times.csv")

        col_headers, row_labels, bike_vals = _read_time_csv(bike_path)
        _, _, drive_vals = _read_time_csv(drive_path)

        out_path = os.path.join(OUTPUT_DIR, f"{city}_delta.csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([""] + col_headers)
            for label, bike_row, drive_row in zip(row_labels, bike_vals, drive_vals):
                delta_row = [
                    (b - d) / d if (b is not None and d is not None and d != 0) else ""
                    for b, d in zip(bike_row, drive_row)
                ]
                writer.writerow([label] + delta_row)

        print(f"Wrote {out_path}")



if __name__ == "__main__":
    compute_diff_over_drive()