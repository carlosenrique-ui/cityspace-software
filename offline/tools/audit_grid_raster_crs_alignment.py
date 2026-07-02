#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – CRS Alignment Auditor
# ==========================================================

import rasterio
import pyogrio
from pathlib import Path

from offline.config.system_paths import GRID_PATH

ENGINE_ROOT = Path(__file__).resolve().parents[2]

RASTER = ENGINE_ROOT / "offline/products/snapshots/ipt_fase1_1cm/z_total_rotated.tif"


def main():

    print("\n==============================================")
    print("IPT-CitySpace – CRS / Alignment Audit")
    print("==============================================")

    print("\n[1/3] Lendo grid científico...")

    gdf = pyogrio.read_dataframe(GRID_PATH)

    grid_bounds = gdf.total_bounds

    print("Grid bounds:")
    print(grid_bounds)

    print("\n[2/3] Lendo raster...")

    with rasterio.open(RASTER) as src:

        raster_bounds = src.bounds

    print("Raster bounds:")
    print(raster_bounds)

    print("\n[3/3] Comparando...")

    dx = abs(grid_bounds[0] - raster_bounds.left)
    dy = abs(grid_bounds[1] - raster_bounds.bottom)

    print("Diferença X:", dx)
    print("Diferença Y:", dy)

    if dx > 1000 or dy > 1000:

        print("\n⚠ DESALINHAMENTO DETECTADO")
        print("Grid provavelmente não está em UTM")

    else:

        print("\n✔ Grid e raster parecem alinhados")

    print("\nAudit finalizado\n")


if __name__ == "__main__":
    main()