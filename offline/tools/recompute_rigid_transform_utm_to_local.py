import json
import numpy as np
from pathlib import Path
import pyogrio

BASE = Path(__file__).resolve().parents[2]

# 🔥 AQUI É A CHAVE
BUILDINGS_UTM = BASE / "offline/data/raw/buildings_original.gpkg"
BUILDINGS_LOCAL = BASE / "offline/products/scientific/buildings_scientific.gpkg"

OUT = BASE / "offline/products/scientific/rigid_transform_utm_to_local.json"


def load_centroids(path):
    gdf = pyogrio.read_dataframe(path)
    return np.array([[g.centroid.x, g.centroid.y] for g in gdf.geometry])


def compute_rigid(A, B):

    A_mean = A.mean(axis=0)
    B_mean = B.mean(axis=0)

    A0 = A - A_mean
    B0 = B - B_mean

    H = A0.T @ B0
    U, S, Vt = np.linalg.svd(H)

    R = Vt.T @ U.T

    angle = np.degrees(np.arctan2(R[1, 0], R[0, 0]))

    return angle, A_mean, B_mean


def main():

    print("\n=== UTM → LOCAL TRANSFORM ===")

    A = load_centroids(BUILDINGS_UTM)
    B = load_centroids(BUILDINGS_LOCAL)

    angle, center_A, center_B = compute_rigid(A, B)

    dx = center_B[0] - center_A[0]
    dy = center_B[1] - center_A[1]

    params = {
        "rotation_deg": float(angle),
        "cx": float(center_A[0]),
        "cy": float(center_A[1]),
        "tx": float(dx),
        "ty": float(dy),
        "transform_type": "utm_to_local"
    }

    with open(OUT, "w") as f:
        json.dump(params, f, indent=2)

    print(json.dumps(params, indent=2))


if __name__ == "__main__":
    main()