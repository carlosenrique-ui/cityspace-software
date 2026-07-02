"""
IPT-CitySpace
CÁLCULO NDSM
"""

import rasterio
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]

DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_CLEAN.tif"
DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_Z.tif"

NDSM = BASE / "offline/data/processed/dsm/IPT_2018_NDSM.tif"

print("\n==============================")
print("CÁLCULO NDSM")
print("==============================\n")

with rasterio.open(DSM) as dsm:
d = dsm.read(1)
meta = dsm.meta.copy()

with rasterio.open(DTM) as dtm:
t = dtm.read(1)

ndsm = d - t
ndsm[ndsm < 0] = 0

with rasterio.open(NDSM,"w",**meta) as dst:
dst.write(ndsm,1)

print("✔ NDSM gerado\n")
