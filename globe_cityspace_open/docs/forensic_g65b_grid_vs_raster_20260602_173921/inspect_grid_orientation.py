from pathlib import Path
import json
import numpy as np

GRID = Path("globe_cityspace_open/projects/ipt_north_5000/grid_z_total_m.csv")
PIN = Path("globe_cityspace_open/projects/ipt_north_5000/grid_pino_cm.csv")

z = np.loadtxt(GRID, delimiter=";")
p = np.loadtxt(PIN, delimiter=";")

def cell_id(r, c):
    return f"P{c*8 + r + 1:03d}"

points = {
    "upper_left": (0, 0),
    "upper_right": (0, 15),
    "lower_left": (7, 0),
    "lower_right": (7, 15),
    "center_approx": (4, 8),
}

report = {
    "grid_shape": z.shape,
    "z_total_min": float(np.nanmin(z)),
    "z_total_max": float(np.nanmax(z)),
    "pin_min": float(np.nanmin(p)),
    "pin_max": float(np.nanmax(p)),
    "sample_cells": {}
}

for name, (r, c) in points.items():
    report["sample_cells"][name] = {
        "row": r + 1,
        "col": c + 1,
        "cell_id_column_zigzag": cell_id(r, c),
        "z_total_m": float(z[r, c]),
        "pin_cm": float(p[r, c]),
    }

report["row_sums_z_total"] = [round(float(v), 3) for v in np.nansum(z, axis=1)]
report["col_sums_z_total"] = [round(float(v), 3) for v in np.nansum(z, axis=0)]

# Compare simple transforms with itself just to list signatures
transforms = {
    "original": z,
    "flipud": np.flipud(z),
    "fliplr": np.fliplr(z),
    "rot180": np.rot90(z, 2),
    "transpose": z.T,
}

report["transform_signatures"] = {}
for name, arr in transforms.items():
    report["transform_signatures"][name] = {
        "shape": arr.shape,
        "upper_left": float(arr[0, 0]),
        "upper_right": float(arr[0, -1]),
        "lower_left": float(arr[-1, 0]),
        "lower_right": float(arr[-1, -1]),
    }

print(json.dumps(report, indent=2, ensure_ascii=False))
