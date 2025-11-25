"""
demo4.py
Demo-only: simulate taking detection outputs and converting them to JSON + a summary.
No real model, no real coordinates – this just mimics a post-processing step.
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List


def read_detections_csv(csv_path: str = "detections/detections_demo.csv") -> List[Dict]:
    path = Path(csv_path).resolve()
    if not path.exists():
        print(f"[demo4] No detections CSV found at {path}.")
        print("[demo4] For demo, create detections/detections_demo.csv manually.")
        return []

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"[demo4] Loaded {len(rows)} detection rows from {path}")
    return rows


def detections_to_json(rows: List[Dict], out_dir: str = "detections/json") -> None:
    out_path = Path(out_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    by_image = defaultdict(list)
    for row in rows:
        by_image[row["image"]].append(row)

    for image_name, dets in by_image.items():
        data = {
            "image": image_name,
            "detections": dets,
            "note": "Demo detection file – values are fake.",
        }
        json_path = out_path / (Path(image_name).stem + "_detections.json")
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[demo4] Wrote detection JSON: {json_path}")


def summarize_detections(rows: List[Dict], out_csv: str = "exports/detection_summary.csv") -> None:
    out_path = Path(out_csv).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    counts = defaultdict(int)
    for row in rows:
        counts[row.get("label", "unknown")] += 1

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "count"])
        for label, count in sorted(counts.items(), key=lambda x: x[0]):
            writer.writerow([label, count])

    print(f"[demo4] Wrote detection summary: {out_path}")


if __name__ == "__main__":
    rows = read_detections_csv()
    if rows:
        detections_to_json(rows)
        summarize_detections(rows)
