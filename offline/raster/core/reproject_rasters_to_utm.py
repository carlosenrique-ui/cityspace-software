"""
IPT-CitySpace
Reprojeção dos rasters originais
4326 -> UTM 23S (EPSG:31983)
"""

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pathlib import Path

print("\n========================================")
print("IPT-CitySpace – REPROJECT RASTERS")
print("========================================\n")

BASE = Path(__file__).resolve().parents[3]

DSM_IN = BASE / "offline/data/raw/IPT-2018-DSM.tif"
DTM_IN = BASE / "offline/data/raw/IPT-2018-DTM.tif"

DSM_OUT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_UTM23S.tif"
DTM_OUT = BASE / "offline/data/processed/dtm/IPT_2018_DTM_UTM23S.tif"

TARGET_CRS = "EPSG:31983"


def reproject_raster(src_path, dst_path):

    print("\nReprojetando:", src_path.name)

    with rasterio.open(src_path) as src:

        transform, width, height = calculate_default_transform(
            src.crs,
            TARGET_CRS,
            src.width,
            src.height,
            *src.bounds
        )

        profile = src.profile.copy()

        profile.update(
            crs=TARGET_CRS,
            transform=transform,
            width=width,
            height=height
        )

        with rasterio.open(dst_path, "w", **profile) as dst:

            for i in range(1, src.count + 1):

                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=TARGET_CRS,
                    resampling=Resampling.bilinear
                )

    print("✔ Criado:", dst_path.name)


reproject_raster(DSM_IN, DSM_OUT)
reproject_raster(DTM_IN, DTM_OUT)

print("\n========================================")
print("REPROJEÇÃO FINALIZADA")
print("========================================\n")