"""
demo1.py
Demo-only: initialize a simple folder structure for an aerial detection pipeline.
No real geospatial or ML logic here – this is just a portfolio example.
"""

import json
from pathlib import Path

FOLDERS = [
    "raw",        # where the original imagery would go
    "tiles",      # where tiled images + metadata would be stored
    "labels",     # manual labels or generated labels
    "detections", # model outputs
    "exports",    # final joined / cleaned results
]

CONFIG_FILE = "project_config.json"


def init_project(root: str = ".") -> None:
    root_path = Path(root).resolve()
    print(f"[demo1] Initializing project at: {root_path}")

    # create folders
    for folder in FOLDERS:
        path = root_path / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"[demo1] Ensured folder: {path}")

    # write a tiny config so people see something concrete
    config_path = root_path / CONFIG_FILE
    if not config_path.exists():
        config = {
            "description": "Demo aerial detection pipeline (fake example).",
            "folders": FOLDERS,
            "note": "This is a demo layout only, real pipeline is private.",
        }
        config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"[demo1] Wrote config: {config_path}")
    else:
        print(f"[demo1] Config already exists: {config_path}")


def check_integrity(root: str = ".") -> None:
    root_path = Path(root).resolve()
    print(f"[demo1] Checking integrity at: {root_path}")

    missing = []
    for folder in FOLDERS:
        path = root_path / folder
        if not path.exists() or not path.is_dir():
            missing.append(folder)

    if missing:
        print(f"[demo1] Missing folders: {', '.join(missing)}")
    else:
        print("[demo1] All expected folders are present.")

    config_path = root_path / CONFIG_FILE
    if not config_path.exists():
        print("[demo1] WARNING: project_config.json is missing.")
    else:
        print(f"[demo1] Found config: {config_path}")


if __name__ == "__main__":
    # Small CLI for demo purposes
    import argparse

    parser = argparse.ArgumentParser(description="Demo project bootstrapper")
    parser.add_argument(
        "action",
        choices=["init", "check"],
        help="init = create folders; check = check integrity",
    )
    args = parser.parse_args()

    if args.action == "init":
        init_project()
    else:
        check_integrity()
