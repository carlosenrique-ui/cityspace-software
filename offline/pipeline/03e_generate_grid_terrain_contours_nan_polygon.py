from pathlib import Path
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, mapping
from scipy.ndimage import zoom, gaussian_filter
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]

GRID_PATH = BASE / "offline/products/scientific/grid_metrics_utm.csv"
POLYGON_PATH = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

OUT_GEOJSON = BASE / "offline/products/scientific/curvas_grid_terrain_2m_nan_polygon.geojson"
OUT_MASK_NPY = BASE / "offline/products/scientific/grid_terrain_nan_polygon.npy"

ROWS = 8
COLS = 16
UPSCALE = 30
INTERVAL_M = 2.0
SMOOTH_SIGMA = 1.0

print("========================================")
print("GRID TERRAIN CONTOURS — FIX")
print("========================================")

df = pd.read_csv(GRID_PATH)

grid = (
    df.pivot(index="row", columns="col", values="z_terrain_m")
    .reindex(index=range(ROWS), columns=range(COLS))
    .values
    .astype(float)
)

poly = gpd.read_file(POLYGON_PATH).dissolve().geometry.iloc[0]
minx, miny, maxx, maxy = gpd.read_file(POLYGON_PATH).total_bounds

# =========================================
# MÁSCARA NO GRID
# =========================================

mask = np.zeros((ROWS, COLS), dtype=bool)

for r in range(ROWS):
    for c in range(COLS):
        x = minx + ((c + 0.5) / COLS) * (maxx - minx)
        y = maxy - ((r + 0.5) / ROWS) * (maxy - miny)
        mask[r, c] = poly.contains(Point(x, y))

print("Dentro polígono:", mask.sum(), "/", ROWS * COLS)

# =========================================
# INTERPOLAÇÃO SEM NAN
# =========================================

fine = zoom(grid, UPSCALE, order=3)
fine = gaussian_filter(fine, sigma=SMOOTH_SIGMA)

# =========================================
# GERAR MÁSCARA FINA DIRETO NO POLIGONO
# evita cortes quadriculados do grid 8x16
# =========================================

ny, nx = fine.shape
mask_fine = np.zeros((ny, nx), dtype=bool)

for rr in range(ny):
    for cc in range(nx):
        gx = cc / (nx - 1) * (COLS - 1)
        gy = rr / (ny - 1) * (ROWS - 1)

        xw = minx + ((gx + 0.5) / COLS) * (maxx - minx)
        yw = maxy - ((gy + 0.5) / ROWS) * (maxy - miny)

        mask_fine[rr, cc] = poly.contains(Point(xw, yw))

# aplicar NaN depois
fine[~mask_fine] = np.nan

np.save(OUT_MASK_NPY, fine)

# =========================================
# CONTOURS
# =========================================

ny, nx = fine.shape
x = np.linspace(0, COLS - 1, nx)
y = np.linspace(0, ROWS - 1, ny)
X, Y = np.meshgrid(x, y)

zmin = np.nanmin(fine)
zmax = np.nanmax(fine)

levels = np.arange(
    np.ceil(zmin / INTERVAL_M) * INTERVAL_M,
    zmax + INTERVAL_M,
    INTERVAL_M
)

fig, ax = plt.subplots()
cs = ax.contour(X, Y, fine, levels=levels)
plt.close(fig)

features = []

for level, segments in zip(cs.levels, cs.allsegs):
    for coords in segments:
        if len(coords) < 2:
            continue

        line = LineString(coords).simplify(0.02, preserve_topology=True)

        if not line.is_empty:
            features.append({
                "type": "Feature",
                "properties": {"elevation": float(level)},
                "geometry": mapping(line),
            })

geojson = {"type": "FeatureCollection", "features": features}

OUT_GEOJSON.write_text(json.dumps(geojson))

print("========================================")
print("OUTPUT:", OUT_GEOJSON)
print("features:", len(features))
print("========================================")
