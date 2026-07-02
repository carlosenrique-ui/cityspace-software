import geopandas as gpd
import numpy as np
from pathlib import Path

print("========================================")
print("RECOMPUTE ROTATION (GRID vs GRID)")
print("========================================")

# =========================================
# INPUTS
# =========================================
BASE = Path("offline/products/scientific")

# grid original (antes da rotação - se tiver)
# se não tiver, usamos inferência pelo próprio grid
GRID_PATH = BASE / "grid_8x16_metric.gpkg"

if not GRID_PATH.exists():
    raise Exception(f"❌ Grid não encontrado: {GRID_PATH}")

gdf = gpd.read_file(GRID_PATH, engine="pyogrio")

# =========================================
# CENTRÓIDES
# =========================================
gdf["cx"] = gdf.geometry.centroid.x
gdf["cy"] = gdf.geometry.centroid.y

gdf = gdf.sort_values(["row","col"])

coords = gdf[["cx","cy"]].values

# =========================================
# CENTRALIZAR
# =========================================
mean = coords.mean(axis=0)
coords_centered = coords - mean

# =========================================
# PCA → DIREÇÃO PRINCIPAL
# =========================================
U, S, Vt = np.linalg.svd(coords_centered)

# direção principal
direction = Vt[0]

angle_rad = np.arctan2(direction[1], direction[0])
angle_deg = np.degrees(angle_rad)

print("========================================")
print("📐 ANGLE DETECTED")
print("========================================")

print(f"Angle (deg): {angle_deg:.6f}")

# normalizar para [0,360]
angle_norm = angle_deg % 360
print(f"Angle normalized: {angle_norm:.6f}")

# =========================================
# OUTPUT JSON
# =========================================
out = {
    "rotation_detected_deg": float(angle_norm),
    "method": "PCA_on_grid"
}

out_path = BASE / "rotation_detected.json"

import json
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print("\n✅ Saved:", out_path)

