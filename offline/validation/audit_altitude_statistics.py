"""
IPT-CitySpace
AUDITORIA ALTIMÉTRICA
Analisa valores DSM e DTM
"""

import rasterio
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

DSM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_ROT.tif"
DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_ROT.tif"

print("\n==============================")
print("AUDITORIA ALTIMÉTRICA")
print("==============================\n")

def stats(name, path):


with rasterio.open(path) as src:

    data = src.read(1)
    data = data[data != src.nodata]

    print(name)
    print("min :", np.min(data))
    print("max :", np.max(data))
    print("mean:", np.mean(data))
    print("std :", np.std(data))
    print()


stats("DSM", DSM)
stats("DTM", DTM)

print("✔ Estatísticas calculadas\n")
