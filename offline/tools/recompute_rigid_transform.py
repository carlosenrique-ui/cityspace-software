"""
=================================================
IPT CitySpace – RECOMPUTE RIGID TRANSFORM
=================================================

✔ sem geopandas
✔ sem fiona
✔ usa pyogrio + shapely
"""

import json
import numpy as np
from pathlib import Path

from shapely.geometry import shape
import pyogrio


BASE = Path(__file__).resolve().parents[2]

BUILDINGS = BASE / "offline/products/scientific/buildings_scientific.gpkg"
BUILDINGS_ROT = BASE / "offline/products/scientific/buildings_scientific_rotated.gpkg"

OUT = BASE / "offline/products/scientific/rigid_transform_params.json"


# ------------------------------------------------
# carregar geometrias
# ------------------------------------------------

def load_centroids(path):

    geoms = pyogrio.read_dataframe(path)

    centroids = []

    for g in geoms.geometry:
        c = g.centroid
        centroids.append([c.x, c.y])

    return np.array(centroids)


# ------------------------------------------------
# calcular rotação via SVD
# ------------------------------------------------

def compute_rotation(A, B):

    A0 = A - A.mean(axis=0)
    B0 = B - B.mean(axis=0)

    H = A0.T @ B0

    U, S, Vt = np.linalg.svd(H)

    R = Vt.T @ U.T

    angle = np.degrees(np.arctan2(R[1, 0], R[0, 0]))

    return angle


# ------------------------------------------------
# MAIN
# ------------------------------------------------

def main():

    print("\n==============================")
    print("Recomputing rigid transform")
    print("==============================")

    A = load_centroids(BUILDINGS)
    B = load_centroids(BUILDINGS_ROT)

    angle = compute_rotation(A, B)

    center_A = A.mean(axis=0)
    center_B = B.mean(axis=0)

    dx = center_B[0] - center_A[0]
    dy = center_B[1] - center_A[1]

    params = {

        "theta_rotation_deg": float(angle),

        "midpoint_original": center_A.tolist(),

        "midpoint_after_rotation": center_B.tolist(),

        "dx": float(dx),
        "dy": float(dy),

        "transform_type": "rigid"
    }

    with open(OUT, "w") as f:
        json.dump(params, f, indent=2)

    print("\nRigid transform saved:")
    print(json.dumps(params, indent=2))


if __name__ == "__main__":
    main()