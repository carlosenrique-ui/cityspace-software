#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – Raster Min/Max Audit
# ==========================================================

import rasterio
import numpy as np
from pathlib import Path


RASTERS = [

    "offline/products/snapshots/ipt_fase0/z_terrain_real.tif",
    "offline/products/snapshots/ipt_fase0/z_building_real.tif",
    "offline/products/snapshots/ipt_fase0/z_total_real.tif",

    "offline/products/snapshots/ipt_fase1_1cm/z_total_rotated.tif"

]


def main():

    print("\n==============================================")
    print("IPT-CitySpace – Raster Min/Max Audit")
    print("==============================================")

    for path in RASTERS:

        p = Path(path)

        if not p.exists():

            print("\nFile not found:", p)
            continue

        with rasterio.open(p) as src:

            data = src.read(1)

        print("\nFILE:", p)
        print("shape:", data.shape)
        print("min:", float(np.nanmin(data)))
        print("max:", float(np.nanmax(data)))


if __name__ == "__main__":
    main()