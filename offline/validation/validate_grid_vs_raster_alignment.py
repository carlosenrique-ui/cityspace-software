"""
Validação de alinhamento:
GRID 8x16 (UTM) vs Raster DTM/DSM
"""

from pathlib import Path
import rasterio
import fiona

BASE = Path(__file__).resolve().parents[2]

GRID_PATH = BASE / "offline/products/scientific/{GRID_GPKG}"
GRID_LAYER = "grid_8x16_metric"

DTM_PATH = BASE / "offline/data/processed/dtm/IPT_2018_DTM_UTM23S.tif"

def main():

    print("\n==============================")
    print("VALIDAÇÃO GRID vs RASTER")
    print("==============================\n")

    # --- Raster ---
    with rasterio.open(DTM_PATH) as src:
        print("RASTER CRS :", src.crs)
        print("RASTER BOUNDS :", src.bounds)
        print()

    # --- Grid ---
    with fiona.open(GRID_PATH, layer=GRID_LAYER) as grid:
        print("GRID CRS :", grid.crs)
        print("GRID BOUNDS :", grid.bounds)

    print("\n==============================\n")

if __name__ == "__main__":
    main()