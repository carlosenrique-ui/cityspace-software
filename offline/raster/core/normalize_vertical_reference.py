"""
IPT-CitySpace
NORMALIZAÇÃO ALTIMÉTRICA
Sincroniza DSM e DTM no mesmo zero
"""

import rasterio
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]

DSM_IN = BASE / "offline/data/processed/dsm/IPT_2018_DSM_ROT.tif"
DTM_IN = BASE / "offline/data/processed/dtm/IPT_2018_DTM_ROT.tif"

DSM_OUT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_Z.tif"
DTM_OUT = BASE / "offline/data/processed/dtm/IPT_2018_DTM_Z.tif"

print("\n==============================")
print("NORMALIZAÇÃO VERTICAL")
print("==============================\n")

with rasterio.open(DTM_IN) as dtm:


dtm_data = dtm.read(1)
meta = dtm.meta.copy()

valid = dtm_data != dtm.nodata
z0 = np.min(dtm_data[valid])


print("COTA ZERO:", z0)

with rasterio.open(DTM_IN) as src:


data = src.read(1)
data = data - z0

with rasterio.open(DTM_OUT, "w", **meta) as dst:
    dst.write(data,1)


with rasterio.open(DSM_IN) as src:


data = src.read(1)
data = data - z0

with rasterio.open(DSM_OUT, "w", **meta) as dst:
    dst.write(data,1)


print("✔ DSM e DTM sincronizados\n")
