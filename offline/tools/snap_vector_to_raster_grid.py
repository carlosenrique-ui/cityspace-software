"""
Snap vector geometries to raster grid
Robust version (pyogrio + shapely)
Compatible with NumPy 2
"""

from pathlib import Path
import rasterio
import pyogrio
import shapely
import shapely.ops


BASE = Path(__file__).resolve().parents[2]

RASTER = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"

BUILDINGS = BASE / "offline/products/scientific/buildings_scientific_rotated.gpkg"
ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"


def snap_geom(geom, resx, resy):

    def snap_coords(x, y, z=None):
        xs = round(x / resx) * resx
        ys = round(y / resy) * resy
        return (xs, ys)

    return shapely.ops.transform(snap_coords, geom)


def process_layer(path, resx, resy):

    print("Processing:", path)

    gdf = pyogrio.read_dataframe(path)

    new_geoms = []

    for geom in gdf.geometry:

        new_geom = snap_geom(geom, resx, resy)
        new_geoms.append(new_geom)

    gdf["geometry"] = new_geoms

    pyogrio.write_dataframe(
        gdf,
        path,
        driver="GPKG"
    )

    print("Aligned:", path)


def main():

    print()
    print("======================================")
    print("SNAP VECTOR → RASTER GRID")
    print("======================================")

    with rasterio.open(RASTER) as src:

        resx, resy = src.res

        print("Raster resolution:", resx, resy)

    process_layer(BUILDINGS, resx, resy)
    process_layer(ENVELOPE, resx, resy)

    print()
    print("All vectors aligned to raster grid.")


if __name__ == "__main__":
    main()