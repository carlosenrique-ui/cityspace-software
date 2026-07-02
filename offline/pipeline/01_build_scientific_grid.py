# =========================================
# IPT-CitySpace – GRID BUILDER (SQUARE FIX)
# =========================================

import geopandas as gpd
import numpy as np

ROWS = 8
COLS = 16

INPUT_GPKG = "offline/products/scientific/grid_8x16_metric.gpkg"
OUTPUT_DEBUG = "offline/products/scientific/grid_square_debug.txt"

print(">>> LOAD GRID ORIGINAL")
gdf = gpd.read_file(INPUT_GPKG)

xmin, ymin, xmax, ymax = gdf.total_bounds

dx = xmax - xmin
dy = ymax - ymin

print("\n>>> ORIGINAL DOMAIN")
print("DX:", dx)
print("DY:", dy)

# =========================================
# 🔥 STEP 1 — CALCULAR CÉLULA QUADRADA
# =========================================
cell = max(dx / COLS, dy / ROWS)
cell_x = cell
cell_y = cell

cell = max(cell_x, cell_y)

print("\n>>> CELL ORIGINAL")
print("cell_x:", cell_x)
print("cell_y:", cell_y)

print("\n>>> CELL FINAL (SQUARE)")
print("cell:", cell)

# =========================================
# 🔥 STEP 2 — NOVO DOMÍNIO
# =========================================
new_dx = cell * COLS
new_dy = cell * ROWS

offset_x = (new_dx - dx) / 2
offset_y = (new_dy - dy) / 2

xmin_new = xmin - offset_x
xmax_new = xmax + offset_x

ymin_new = ymin - offset_y
ymax_new = ymax + offset_y

print("\n>>> NEW DOMAIN")
print("DX:", new_dx)
print("DY:", new_dy)

print("\n>>> OFFSET")
print("offset_x:", offset_x)
print("offset_y:", offset_y)

# =========================================
# 🔥 STEP 3 — GERAR GRID QUADRADO (COORDENADAS)
# =========================================
grid_cells = []

for r in range(ROWS):
    for c in range(COLS):
        x0 = xmin_new + c * cell
        x1 = x0 + cell

        y0 = ymin_new + r * cell
        y1 = y0 + cell

        grid_cells.append((r, c, x0, y0, x1, y1))

print("\n>>> TOTAL CELLS:", len(grid_cells))

# =========================================
# DEBUG SAVE
# =========================================
with open(OUTPUT_DEBUG, "w") as f:
    for row in grid_cells:
        f.write(str(row) + "\n")

print("\n>>> GRID SQUARE GERADO")
print(">>> PRONTO PARA AMOSTRAGEM DSM/DTM")
