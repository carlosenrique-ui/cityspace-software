import geopandas as gpd
import numpy as np
from pathlib import Path

print("========================================")
print("RECOMPUTE TRUE ROTATION (ORIG vs ROT)")
print("========================================")

BASE = Path("offline")

ORIG = BASE / "data/raw/buildings_original.gpkg"
ROT  = BASE / "products/scientific/buildings_scientific_rotated.gpkg"

if not ORIG.exists():
    raise Exception(f"❌ ORIGINAL não encontrado: {ORIG}")

if not ROT.exists():
    raise Exception(f"❌ ROTATED não encontrado: {ROT}")

gdf_A = gpd.read_file(ORIG, engine="pyogrio")
gdf_B = gpd.read_file(ROT, engine="pyogrio")

# usar centróides
A = np.array([[g.centroid.x, g.centroid.y] for g in gdf_A.geometry])
B = np.array([[g.centroid.x, g.centroid.y] for g in gdf_B.geometry])

# garantir mesmo tamanho
n = min(len(A), len(B))
A = A[:n]
B = B[:n]

# centralizar
A_mean = A.mean(axis=0)
B_mean = B.mean(axis=0)

A_c = A - A_mean
B_c = B - B_mean

# SVD (Procrustes)
H = A_c.T @ B_c
U, S, Vt = np.linalg.svd(H)

R = Vt.T @ U.T

angle = np.degrees(np.arctan2(R[1,0], R[0,0]))

print("========================================")
print("📐 ROTATION DETECTED")
print("========================================")

print(f"Angle (deg): {angle:.6f}")

angle_norm = angle % 360
print(f"Angle normalized: {angle_norm:.6f}")

