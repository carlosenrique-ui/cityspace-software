#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – Scientific Raster Runner
# Método B + Modelo Urbano
# ==========================================================

import rasterio
import numpy as np
import subprocess
import pyogrio

from pathlib import Path
from rasterio.mask import mask
from rasterio.features import rasterize

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

BASE = Path(__file__).resolve().parents[3]

DSM_LOCAL = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM_LOCAL = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"

DSM_CLIP = BASE / "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"
DTM_CLIP = BASE / "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"

HEIGHT = BASE / "offline/data/processed/height/HEIGHT.tif"
HEIGHT_TOTAL = BASE / "offline/data/processed/height/HEIGHT_TOTAL.tif"

ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"
BUILDINGS = BASE / "offline/products/scientific/buildings_scientific_rotated.gpkg"


# ----------------------------------------------------------
# ENVELOPE
# ----------------------------------------------------------

def load_envelope():

    df = pyogrio.read_dataframe(ENVELOPE)

    geom = [df.geometry.iloc[0]]

    print("\n=================================================")
    print("[ENVELOPE]")
    print("=================================================")

    print("Bounds:", df.geometry.iloc[0].bounds)

    return geom


# ----------------------------------------------------------
# CLIP RASTER
# ----------------------------------------------------------

def clip_raster(input_raster, output_raster, geom):

    print("\n=================================================")
    print("[CLIP]", input_raster.name)
    print("=================================================")

    with rasterio.open(input_raster) as src:

        print("Raster bounds:", src.bounds)

        out_image, out_transform = mask(src, geom, crop=True)

        profile = src.profile.copy()

        profile.update(
            height=out_image.shape[1],
            width=out_image.shape[2],
            transform=out_transform
        )

        with rasterio.open(output_raster, "w", **profile) as dst:

            dst.write(out_image)

    print("[OK] Saved:", output_raster.name)


# ----------------------------------------------------------
# BUILDING MASK
# ----------------------------------------------------------

def build_building_mask(reference_raster):

    print("\nBuilding mask from vector")

    df = pyogrio.read_dataframe(BUILDINGS)

    with rasterio.open(reference_raster) as src:

        shapes = [(geom, 1) for geom in df.geometry]

        mask_raster = rasterize(
            shapes,
            out_shape=(src.height, src.width),
            transform=src.transform,
            fill=0,
            dtype="uint8"
        )

    print("Building pixels:", np.sum(mask_raster))

    return mask_raster


# ----------------------------------------------------------
# HEIGHT MODEL (Método B)
# ----------------------------------------------------------

def compute_height_models():

    print("\n=================================================")
    print("[ALTIMETRIA – MÉTODO B]")
    print("=================================================")

    with rasterio.open(DSM_CLIP) as dsm:
        dsm_data = dsm.read(1)
        profile = dsm.profile

    with rasterio.open(DTM_CLIP) as dtm:
        dtm_data = dtm.read(1)

    # ------------------------------------------------------
    # nDSM
    # ------------------------------------------------------

    ndsm = dsm_data - dtm_data

    ndsm[ndsm < 0] = 0
    ndsm[ndsm > 120] = 0

    # ------------------------------------------------------
    # building mask
    # ------------------------------------------------------

    building_mask = build_building_mask(DSM_CLIP)

    ndsm_buildings = ndsm.copy()
    ndsm_buildings[building_mask == 0] = np.nan

    valid = ndsm_buildings[~np.isnan(ndsm_buildings)]

    if len(valid) > 0:
        p90 = np.percentile(valid, 90)
    else:
        p90 = 0

    print("Robust building height p90:", p90)

    # ------------------------------------------------------
    # urban model
    # ------------------------------------------------------

    height = ndsm.copy()

    height[building_mask == 0] = 0

    height_total = dtm_data + height

    profile.update(dtype="float32")

    with rasterio.open(HEIGHT, "w", **profile) as dst:
        dst.write(height.astype("float32"), 1)

    with rasterio.open(HEIGHT_TOTAL, "w", **profile) as dst:
        dst.write(height_total.astype("float32"), 1)

    print("HEIGHT saved:", HEIGHT.name)
    print("HEIGHT_TOTAL saved:", HEIGHT_TOTAL.name)

    print("Height min:", np.nanmin(height))
    print("Height max:", np.nanmax(height))


# ----------------------------------------------------------
# BUILD URBAN GRID
# ----------------------------------------------------------

def build_scientific_grid():

    print("\n=================================================")
    print("[GRID URBANO]")
    print("=================================================")

    subprocess.run(
        ["python", "-m", "offline.scientific_grid_builder"],
        check=True
    )

    subprocess.run(
        ["python", "-m", "offline.scientific_cell_metrics_utm"],
        check=True
    )

    print("\nGrid urbano gerado")


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    print("\n=================================================")
    print("IPT-CitySpace – SCIENTIFIC RASTER RUNNER")
    print("=================================================")

    geom = load_envelope()

    clip_raster(DSM_LOCAL, DSM_CLIP, geom)
    clip_raster(DTM_LOCAL, DTM_CLIP, geom)

    compute_height_models()

    build_scientific_grid()

    print("\n=================================================")
    print("RUNNER FINALIZADO")
    print("=================================================")


if __name__ == "__main__":
    main()