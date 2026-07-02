import rasterio
from rasterio.transform import Affine
import pyogrio
from pathlib import Path

print()
print("===================================")
print("SHIFT RASTER TO ENVELOPE")
print("===================================")

BASE = Path(__file__).resolve().parents[2]

DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"


gdf = pyogrio.read_dataframe(ENVELOPE)
env = gdf.geometry.iloc[0]

env_bottom = env.bounds[1]

with rasterio.open(DSM) as src:

    raster_top = src.bounds.top
    shift_y = env_bottom - raster_top

    print("Envelope bottom:", env_bottom)
    print("Raster top:", raster_top)
    print("Shift Y:", shift_y)

    data = src.read()
    profile = src.profile
    transform = src.transform

new_transform = transform * Affine.translation(0, shift_y)

profile["transform"] = new_transform

with rasterio.open(DSM, "w", **profile) as dst:
    dst.write(data)

with rasterio.open(DTM) as src:
    data = src.read()
    profile = src.profile
    transform = src.transform

new_transform = transform * Affine.translation(0, shift_y)

profile["transform"] = new_transform

with rasterio.open(DTM, "w", **profile) as dst:
    dst.write(data)

print()
print("RASTERS SHIFTED")
