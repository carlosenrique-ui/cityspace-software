from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[2]

terrain_path = BASE / "offline/products/grid_terrain_m.csv"
building_path = BASE / "offline/products/grid_building_m.csv"
total_path = BASE / "offline/products/grid_z_total_m.csv"

out = BASE / "offline/products/scientific/grid_metrics_utm.csv"

ROWS = 8
COLS = 16

print("========================================")
print("BUILD grid_metrics_utm.csv FROM MATRIX CSVs")
print("========================================")

def load_matrix(path):
    print("Lendo:", path)
    arr = np.loadtxt(path, delimiter=";")
    print("shape:", arr.shape, "min:", np.nanmin(arr), "max:", np.nanmax(arr))
    if arr.shape != (ROWS, COLS):
        raise ValueError(f"Shape inválido em {path}: {arr.shape}, esperado {(ROWS, COLS)}")
    return arr

terrain = load_matrix(terrain_path)
building = load_matrix(building_path)
total = load_matrix(total_path)

records = []
for r in range(ROWS):
    for c in range(COLS):
        records.append({
            "row": r,
            "col": c,
            "z_terrain_m": float(terrain[r, c]),
            "z_building_m": float(building[r, c]),
            "z_total_m": float(total[r, c]),
        })

df = pd.DataFrame(records)

out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)

print("========================================")
print("OUTPUT:", out)
print("rows:", len(df))
print(df.head(20).to_string(index=False))
print("========================================")
