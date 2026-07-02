import rasterio
from rasterio.transform import Affine
import pyogrio
from pathlib import Path

print("\n====================================")
print("ALIGN RASTER TO ENVELOPE")
print("====================================\n")

BASE = Path(__file__).resolve().parents[2]

DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

# carregar envelope
gdf = pyogrio.read_dataframe(ENVELOPE)
env_bounds = gdf.geometry.iloc[0].bounds

env_bottom = env_bounds[1]
env_top = env_bounds[3]

print("Envelope bounds:", env_bounds)

def shift_raster(path):

    with rasterio.open(path) as src:

        raster_bounds = src.bounds
        print("\nRaster:", path.name)
        print("Raster bounds:", raster_bounds)

        raster_top = raster_bounds.top

        shift_y = env_bottom - raster_top

        print("Computed shift Y:", shift_y)

        data = src.read()
        profile = src.profile
        transform = src.transform

    new_transform = transform * Affine.translation(0, shift_y)

    profile["transform"] = new_transform

    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data)

    print("Raster shifted.")

shift_raster(DSM)
shift_raster(DTM)

print("\nRASTERS REALIGNED\n")
