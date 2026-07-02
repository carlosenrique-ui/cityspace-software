#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – Coordinate System Auditor
# ==========================================================

import pyogrio
import rasterio

from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

VECTOR = BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"

RASTER = BASE / "offline/products/snapshots/ipt_fase1_1cm/z_total_rotated.tif"


# ----------------------------------------------------------
def check_vector(path):

    gdf = pyogrio.read_dataframe(path)

    xmin, ymin, xmax, ymax = gdf.total_bounds

    print("\nVector:", path)
    print("Bounds:", xmin, ymin, xmax, ymax)
    print("CRS:", gdf.crs)

    return xmin, ymin, xmax, ymax


# ----------------------------------------------------------
def check_raster(path):

    with rasterio.open(path) as src:

        bounds = src.bounds

        print("\nRaster:", path)
        print("Bounds:", bounds)
        print("CRS:", src.crs)

        return bounds.left, bounds.bottom, bounds.right, bounds.top


# ----------------------------------------------------------
def main():

    print("\n===================================")
    print("CitySpace Coordinate Auditor")
    print("===================================")

    v = check_vector(VECTOR)

    r = check_raster(RASTER)

    dx = abs(v[0] - r[0])
    dy = abs(v[1] - r[1])

    print("\nDelta X:", dx)
    print("Delta Y:", dy)

    if dx > 10000 or dy > 10000:

        print("\n⚠ Coordinate mismatch detected")
        print("Vector likely not in UTM")

    else:

        print("\n✔ Coordinates appear consistent")


# ----------------------------------------------------------
if __name__ == "__main__":
    main()