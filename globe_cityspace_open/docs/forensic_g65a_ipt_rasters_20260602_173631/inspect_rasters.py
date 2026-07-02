from pathlib import Path
import json
import numpy as np
import rasterio

files = {
    "DSM_CLIP": "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif",
    "DTM_CLIP": "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif",
    "DSM_LOCAL": "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif",
    "DTM_LOCAL": "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif",
}

report = {}

for name, fp in files.items():
    p = Path(fp)
    item = {"path": fp, "exists": p.exists()}
    if p.exists():
        with rasterio.open(p) as src:
            arr = src.read(1, masked=True)
            item.update({
                "crs": str(src.crs),
                "width": src.width,
                "height": src.height,
                "bounds": tuple(round(v, 3) for v in src.bounds),
                "transform": tuple(round(v, 6) for v in src.transform),
                "nodata": src.nodata,
                "min": float(arr.min()),
                "max": float(arr.max()),
                "mean": float(arr.mean()),
                "pixel_size_x": float(src.transform.a),
                "pixel_size_y": float(src.transform.e),
                "north_up": bool(src.transform.e < 0),
            })
    report[name] = item

pairs = [
    ("DSM_CLIP", "DTM_CLIP"),
    ("DSM_LOCAL", "DTM_LOCAL"),
]

for dsm_name, dtm_name in pairs:
    dsm_path = Path(files[dsm_name])
    dtm_path = Path(files[dtm_name])
    key = f"{dsm_name}_minus_{dtm_name}"
    item = {"available": dsm_path.exists() and dtm_path.exists()}
    if item["available"]:
        with rasterio.open(dsm_path) as dsm, rasterio.open(dtm_path) as dtm:
            a = dsm.read(1, masked=True).astype("float64")
            b = dtm.read(1, masked=True).astype("float64")
            if a.shape == b.shape:
                diff = a - b
                item.update({
                    "shape": a.shape,
                    "min": float(diff.min()),
                    "max": float(diff.max()),
                    "mean": float(diff.mean()),
                    "positive_pixels": int(np.sum(diff.filled(0) > 0)),
                    "nonzero_pixels": int(np.sum(np.abs(diff.filled(0)) > 1e-6)),
                })
            else:
                item["shape_mismatch"] = [a.shape, b.shape]
    report[key] = item

print(json.dumps(report, indent=2, ensure_ascii=False))
