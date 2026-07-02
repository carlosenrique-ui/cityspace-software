import rasterio
from rasterio.transform import Affine
import pyogrio
from pathlib import Path

print("\nREANCHOR RASTER TO ENVELOPE\n")

BASE = Path(__file__).resolve().parents[2]

DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

gdf = pyogrio.read_dataframe(ENVELOPE)
env = gdf.geometry.iloc[0]
env_left, env_bottom, env_right, env_top = env.bounds

def reanchor(path):
    with rasterio.open(path) as src:
        data = src.read()
        profile = src.profile
        px = src.transform.a
        py = src.transform.e

    new_transform = Affine(px, 0, env_left, 0, py, env_top)

    profile["transform"] = new_transform

    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data)

    print("Reanchored:", path.name)

reanchor(DSM)
reanchor(DTM)

print("\nDONE\n")
