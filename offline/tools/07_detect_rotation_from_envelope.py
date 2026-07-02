import geopandas as gpd
import numpy as np
from pathlib import Path

print("========================================")
print("DETECT ROTATION FROM ENVELOPE")
print("========================================")

BASE = Path("offline/products/scientific")

ENV_PATH = BASE / "urban_envelope_scientific_rotated.gpkg"

if not ENV_PATH.exists():
    raise Exception(f"❌ Envelope não encontrado: {ENV_PATH}")

gdf = gpd.read_file(ENV_PATH, engine="pyogrio")

geom = gdf.geometry.iloc[0]

# pegar pontos da borda
coords = np.array(geom.exterior.coords)

# centralizar
mean = coords.mean(axis=0)
coords_centered = coords - mean

# PCA
U, S, Vt = np.linalg.svd(coords_centered)

direction = Vt[0]

angle_rad = np.arctan2(direction[1], direction[0])
angle_deg = np.degrees(angle_rad)

angle_norm = angle_deg % 360

print("========================================")
print("📐 ANGLE DETECTED")
print("========================================")

print(f"Angle (deg): {angle_deg:.6f}")
print(f"Angle normalized: {angle_norm:.6f}")

# salvar
import json
out = {
    "rotation_detected_deg": float(angle_norm),
    "source": "envelope_pca"
}

out_path = BASE / "rotation_from_envelope.json"

with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print("\n✅ Saved:", out_path)

