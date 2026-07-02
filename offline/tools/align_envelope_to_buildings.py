"""
IPT-CitySpace
Align urban envelope to buildings (centroid-based correction)
"""

import pyogrio
from shapely.affinity import translate
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific.gpkg"
BUILDINGS = BASE / "offline/products/scientific/buildings_scientific.gpkg"

OUTPUT = BASE / "offline/products/scientific/urban_envelope_scientific.gpkg"


def compute_global_centroid(gdf):
    merged = gdf.geometry.unary_union
    return merged.centroid


def main():

    print("\n==========================================")
    print("Align Envelope to Buildings (Centroid)")
    print("==========================================\n")

    print("[1/4] Loading data...")

    env = pyogrio.read_dataframe(ENVELOPE)
    bld = pyogrio.read_dataframe(BUILDINGS)

    print("[2/4] Computing centroids...")

    c_env = compute_global_centroid(env)
    c_bld = compute_global_centroid(bld)

    print(f"Envelope centroid: ({c_env.x:.3f}, {c_env.y:.3f})")
    print(f"Buildings centroid: ({c_bld.x:.3f}, {c_bld.y:.3f})")

    dx = c_bld.x - c_env.x
    dy = c_bld.y - c_env.y

    print(f"\nOffset detected:")
    print(f"dx = {dx:.6f}")
    print(f"dy = {dy:.6f}")

    print("\n[3/4] Applying correction...")

    new_geoms = []

    for geom in env.geometry:
        g = translate(geom, xoff=dx, yoff=dy)
        new_geoms.append(g)

    env.geometry = new_geoms

    print("\n[4/4] Saving...")

    pyogrio.write_dataframe(env, OUTPUT)

    print("\nSaved corrected envelope.")
    print(OUTPUT)

    print("\nDone.\n")


if __name__ == "__main__":
    main()