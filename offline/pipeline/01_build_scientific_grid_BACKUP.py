import numpy as np
import pandas as pd
from pathlib import Path

ROWS=8
COLS=16

OUT=Path("offline/products/scientific")
OUT.mkdir(parents=True,exist_ok=True)

data=[]

for r in range(ROWS):
    for c in range(COLS):
        zt=np.random.uniform(0,30)
        zb=np.random.uniform(0,20) if np.random.rand()>0.6 else 0
        data.append([r,c,zt,zb,zt+zb])

df=pd.DataFrame(data,columns=["row","col","z_terrain_m","z_building_m","z_total_m"])
df.to_csv(OUT/"grid_metrics_utm.csv",index=False)

print("OK CSV")
