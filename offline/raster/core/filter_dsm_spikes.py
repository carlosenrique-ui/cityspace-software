"""
IPT-CitySpace
LIMPEZA DSM
Remove picos (galhos, antenas)
"""

import rasterio
import numpy as np
from scipy.ndimage import median_filter
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]

DSM_IN = BASE / "offline/data/processed/dsm/IPT_2018_DSM_Z.tif"
DSM_OUT = BASE / "offline/data/processed/dsm/IPT_2018_DSM_CLEAN.tif"

print("\n==============================")
print("LIMPEZA DSM")
print("==============================\n")

with rasterio.open(DSM_IN) as src:


data = src.read(1)
meta = src.meta.copy()

filtered = median_filter(data, size=3)

cleaned = np.minimum(data, filtered)

with rasterio.open(DSM_OUT, "w", **meta) as dst:
    dst.write(cleaned,1)


print("✔ DSM limpo\n")
