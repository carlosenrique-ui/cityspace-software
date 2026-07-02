"""
IPT-CitySpace
AUDIT RASTER ALIGNMENT

Verifica alinhamento entre DTM e DSM
"""

from pathlib import Path
import rasterio

print("\n===================================")
print("IPT-CitySpace – RASTER ALIGNMENT AUDIT")
print("===================================\n")

BASE = Path(__file__).resolve().parents[2]

DTM_PATH = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
DSM_PATH = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"

print("DTM:", DTM_PATH)
print("DSM:", DSM_PATH)

print("\n--- DTM ---")

with rasterio.open(DTM_PATH) as dtm:

    print("bounds:", dtm.bounds)
    print("width:", dtm.width)
    print("height:", dtm.height)
    print("resolution:", dtm.res)
    print("crs:", dtm.crs)


print("\n--- DSM ---")

with rasterio.open(DSM_PATH) as dsm:


    print("bounds:", dsm.bounds)
    print("width:", dsm.width)
    print("height:", dsm.height)
    print("resolution:", dsm.res)
    print("crs:", dsm.crs)


print("\n===================================")
print("AUDIT FINALIZADO")
print("===================================\n")
