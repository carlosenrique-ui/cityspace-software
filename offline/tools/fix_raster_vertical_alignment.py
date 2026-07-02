import rasterio
from rasterio.transform import Affine
import pyogrio
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"

ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"


def compute_offset():

    env = pyogrio.read_dataframe(ENVELOPE)

    env_bounds = env.geometry.iloc[0].bounds

    env_bottom = env_bounds[1]

    with rasterio.open(DSM) as src:
        raster_top = src.bounds.top

    dy = env_bottom - raster_top

    print("Envelope bottom:", env_bottom)
    print("Raster top:", raster_top)
    print("Computed shift Y:", dy)

    return dy


def shift_raster(path, dy):

    with rasterio.open(path) as src:

        transform = src.transform

        new_transform = transform * Affine.translation(0, -dy)

        profile = src.profile.copy()
        profile["transform"] = new_transform

        data = src.read()

    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data)


def main():

    print("\nALIGNING RASTERS TO ENVELOPE\n")

    dy = compute_offset()

    shift_raster(DSM, dy)
    shift_raster(DTM, dy)

    print("\nDONE\n")


if __name__ == "__main__":
    main()