"""
IPT-CitySpace
Audit Lowest Points of DTM and DSM

Identifica:

• ponto mais baixo do terreno
• ponto mais baixo da superfície
• coordenadas geográficas
• distância entre os dois
"""

from pathlib import Path
import rasterio
import numpy as np
from math import sqrt


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

ENGINE_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------
# INPUT RASTERS
# ---------------------------------------------------------

DTM = ENGINE_ROOT / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
DSM = ENGINE_ROOT / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"


# ---------------------------------------------------------
# FUNCTION
# ---------------------------------------------------------

def find_lowest(raster_path):

    with rasterio.open(raster_path) as src:

        data = src.read(1)

        # ignorar nodata
        mask = data != src.nodata

        valid = data[mask]

        min_val = np.min(valid)

        # posição do mínimo
        row, col = np.where(data == min_val)

        row = row[0]
        col = col[0]

        # converter para coordenada
        x, y = src.xy(row, col)

        return min_val, row, col, x, y


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("\n===================================")
    print("CITYSPACE – LOWEST POINT AUDIT")
    print("===================================\n")

    dtm_val, dtm_r, dtm_c, dtm_x, dtm_y = find_lowest(DTM)
    dsm_val, dsm_r, dsm_c, dsm_x, dsm_y = find_lowest(DSM)

    print("DTM lowest point")
    print("-----------------")
    print("value :", dtm_val)
    print("row   :", dtm_r)
    print("col   :", dtm_c)
    print("x     :", dtm_x)
    print("y     :", dtm_y)

    print("\nDSM lowest point")
    print("-----------------")
    print("value :", dsm_val)
    print("row   :", dsm_r)
    print("col   :", dsm_c)
    print("x     :", dsm_x)
    print("y     :", dsm_y)

    # distância entre pontos

    dx = dsm_x - dtm_x
    dy = dsm_y - dtm_y

    dist = sqrt(dx**2 + dy**2)

    print("\nDistance between lowest points")
    print("--------------------------------")

    print("meters :", dist)

    if dist < 10:
        print("Result : VERY CLOSE")
    elif dist < 50:
        print("Result : CLOSE")
    else:
        print("Result : FAR")


# ---------------------------------------------------------

if __name__ == "__main__":
    main()