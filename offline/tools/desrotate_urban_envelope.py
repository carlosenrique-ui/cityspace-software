"""
IPT-CitySpace
Desrotate envelope WITHOUT altering geometry
"""

import json
import pyogrio
from shapely.affinity import rotate, translate
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

INPUT = BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"
OUTPUT = BASE / "offline/products/scientific/urban_envelope_scientific.gpkg"

PARAMS = BASE / "offline/products/scientific/rigid_transform_params.json"


def main():

    print("\n==========================================")
    print("Desrotate Envelope (Preserve Geometry)")
    print("==========================================\n")

    with open(PARAMS) as f:
        params = json.load(f)

    angle = params["theta_rotation_deg"]
    origin_rot = params["midpoint_after_rotation"]
    origin_target = params["midpoint_original"]

    gdf = pyogrio.read_dataframe(INPUT)

    new_geoms = []

    for geom in gdf.geometry:

        # 1) desrotacionar (centro correto)
        g = rotate(
            geom,
            -angle,
            origin=tuple(origin_rot)
        )

        # 2) corrigir offset global (sem deformar)
        c = g.centroid

        dx = origin_target[0] - c.x
        dy = origin_target[1] - c.y

        g = translate(g, xoff=dx, yoff=dy)

        new_geoms.append(g)

    gdf.geometry = new_geoms

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    pyogrio.write_dataframe(gdf, OUTPUT)

    print("\nSaved:")
    print(OUTPUT)

    print("\nDone.\n")


if __name__ == "__main__":
    main()