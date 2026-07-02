"""
IPT-CitySpace
Apply Rigid Transform to Raster (CORRECT)
"""

from pathlib import Path
import json
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import Affine


BASE = Path(__file__).resolve().parents[2]

DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_UTM23S.tif"
DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_UTM23S.tif"

PARAMS = BASE / "offline/products/scientific/rigid_transform_utm_to_local.json"

OUT_DTM = BASE / "offline/products/scientific/dtm_local.tif"
OUT_DSM = BASE / "offline/products/scientific/dsm_local.tif"


def build_affine(p):

    angle = p["rotation_deg"]
    cx = p["cx"]
    cy = p["cy"]
    tx = p["tx"]
    ty = p["ty"]

    T1 = Affine.translation(-cx, -cy)
    R = Affine.rotation(angle)
    T2 = Affine.translation(cx + tx, cy + ty)

    return T2 * R * T1


def transform_raster(src_path, dst_path, affine):

    with rasterio.open(src_path) as src:

        data = src.read(1)

        # criar grid destino (mesmo tamanho por enquanto)
        dst_data = np.zeros_like(data)

        dst_transform = affine * src.transform

        reproject(
            source=data,
            destination=dst_data,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=src.crs,
            resampling=Resampling.bilinear
        )

        with rasterio.open(
            dst_path,
            "w",
            driver="GTiff",
            height=src.height,
            width=src.width,
            count=1,
            dtype=dst_data.dtype,
            crs=src.crs,
            transform=dst_transform,
        ) as dst:

            dst.write(dst_data, 1)


def main():

    print("\n==========================================")
    print("Apply Rigid Transform to Raster (FIXED)")
    print("==========================================\n")

    with open(PARAMS) as f:
        params = json.load(f)

    affine = build_affine(params)

    print("Transforming DTM...")
    transform_raster(DTM, OUT_DTM, affine)

    print("Transforming DSM...")
    transform_raster(DSM, OUT_DSM, affine)

    print("\nDone.")


if __name__ == "__main__":
    main()