"""
demo3
Demo-only: create fake labels for tiles and export a tiny YOLO-style dataset.
No real labeling logic – this is just to show the idea of a training pack step.
"""

import json
from pathlib import Path
from typing import List, Dict


def list_tiles(tiles_dir: str = "tiles") -> List[Path]:
    path = Path(tiles_dir).resolve()
    return [p for p in path.glob("*_tile_0.*") if p.is_file()]


def create_fake_label(image_name: str) -> Dict:
    """
    Return a tiny fake annotation structure compatible with many CV tools.
    This is not based on any real detections.
    """
    return {
        "imagePath": image_name,
        "shapes": [
            {
                "label": "demo_object",
                "points": [
                    [10, 10],
                    [100, 100],
                ],
                "shape_type": "rectangle",
            }
        ],
        "note": "Demo label – not real data.",
    }


def generate_labels(tiles_dir: str = "tiles", labels_dir: str = "labels") -> None:
    tiles = list_tiles(tiles_dir)
    labels_path = Path(labels_dir).resolve()
    labels_path.mkdir(parents=True, exist_ok=True)

    if not tiles:
        print("[demo3] No tiles found. Run demo2.py first.")
        return

    for tile in tiles:
        label = create_fake_label(tile.name)
        label_path = labels_path / (tile.stem + ".json")
        label_path.write_text(json.dumps(label, indent=2), encoding="utf-8")
        print(f"[demo3] Wrote fake label: {label_path.name}")


def export_yolo_dataset(labels_dir: str = "labels", export_dir: str = "exports/yolo_demo") -> None:
    """
    Create a tiny YOLO-style folder layout using the tiles + fake labels.
    This is intentionally minimal and not tied to any real project.
    """
    labels_path = Path(labels_dir).resolve()
    export_root = Path(export_dir).resolve()
    images_train = export_root / "images" / "train"
    labels_train = export_root / "labels" / "train"

    images_train.mkdir(parents=True, exist_ok=True)
    labels_train.mkdir(parents=True, exist_ok=True)

    # For demo, just copy label JSON filenames to a "labels.txt"-like placeholder.
    json_files = list(labels_path.glob("*.json"))
    if not json_files:
        print("[demo3] No labels found. Run generate_labels() first.")
        return

    for jf in json_files:
        # In a real pipeline this would convert JSON → YOLO txt,
        # here we just copy the JSON so people see the structure.
        fake_yolo_label = labels_train / (jf.stem + ".txt")
        fake_yolo_label.write_text("# demo placeholder for YOLO labels\n", encoding="utf-8")
        print(f"[demo3] Created placeholder YOLO label: {fake_yolo_label}")

    # Minimal data.yaml
    data_yaml = export_root / "data.yaml"
    data_yaml.write_text(
        "path: .\n"
        "train: images/train\n"
        "val: images/train  # demo: using train as val\n"
        "names:\n"
        "  0: demo_object\n",
        encoding="utf-8",
    )
    print(f"[demo3] Wrote demo data.yaml: {data_yaml}")


if __name__ == "__main__":
    generate_labels()
    export_yolo_dataset()
