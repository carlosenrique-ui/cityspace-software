import geopandas as gpd
import numpy as np
from pathlib import Path

print("========================================")
print("GENERATE GRID.NPY FROM GPKG")
print("========================================")

BASE = Path("offline/products/scientific")

GPKG = BASE / "grid_8x16_metric.gpkg"
OUT  = BASE / "grid.npy"

if not GPKG.exists():
    raise Exception(f"❌ GPKG não encontrado: {GPKG}")

gdf = gpd.read_file(GPKG, engine="pyogrio")

print("Loaded:", gdf.shape)

# garantir ordenação
gdf = gdf.sort_values(["row", "col"])

rows = int(gdf["row"].max() + 1)
cols = int(gdf["col"].max() + 1)

print("Grid size:", rows, cols)

# criar matriz dummy (pode evoluir depois)
grid = np.zeros((rows, cols))

for _, r in gdf.iterrows():
    grid[int(r["row"]), int(r["col"])] = 1

np.save(OUT, grid)

print("✅ grid.npy gerado:", OUT)
