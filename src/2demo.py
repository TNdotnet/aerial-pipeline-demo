"""
demo2.py
Demo-only: simulate converting raw images into tiles with simple metadata.
No formats, no real coordinates – this is just to show structure.
"""

import json
import shutil
from pathlib import Path


def generate_tiles(raw_dir: str = "raw", tiles_dir: str = "tiles") -> None:
    raw_path = Path(raw_dir).resolve()
    tiles_path = Path(tiles_dir).resolve()

    tiles_path.mkdir(parents=True, exist_ok=True)

    # For the demo, treat any file in raw/ as an "image"
    raw_files = [p for p in raw_path.iterdir() if p.is_file()]
    if not raw_files:
        print("[demo2] No files found in 'raw'. Put some dummy images/files there.")
        return

    for src in raw_files:
        # fake "tiling": we just make one tile per file and copy it
        tile_name = src.stem + "_tile_0" + src.suffix
        dst = tiles_path / tile_name

        shutil.copy2(src, dst)
        print(f"[demo2] Created tile: {dst.name}")

        # write simple metadata next to it
        meta = {
            "source_file": src.name,
            "tile_file": dst.name,
            "fake_crs": "EPSG:4326",
            "fake_bounds": {
                "min_lat": 0.0,
                "min_lon": 0.0,
                "max_lat": 1.0,
                "max_lon": 1.0,
            },
            "note": "Demo metadata only – real geospatial logic is private.",
        }
        meta_path = tiles_path / (dst.stem + "_meta.json")
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"[demo2] Wrote meta: {meta_path.name}")


if __name__ == "__main__":
    generate_tiles()
