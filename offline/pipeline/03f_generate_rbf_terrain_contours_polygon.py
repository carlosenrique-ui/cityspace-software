from pathlib import Path
import json
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, mapping
from shapely.ops import unary_union
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[2]

GRID_GPKG = BASE / "offline/products/scientific/grid_8x16_enriched.gpkg"
POLY_SRC = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

OUT_POLY = BASE / "offline/products/scientific/poligono_urbanismo_ipt_outer_real.gpkg"
OUT_GEOJSON = BASE / "offline/products/scientific/curvas_rbf_terrain_2m_real.geojson"
OUT_SURFACE = BASE / "offline/products/scientific/rbf_terrain_surface_real.npz"

INTERVAL_M = 2.0
NX = 700
NY = 360
SMOOTH_SIGMA = 1.0
POLYGON_SHRINK_M = 0.0

print("========================================")
print("V110 REAL — RBF em cx/cy UTM")
print("========================================")

grid = gpd.read_file(GRID_GPKG)
poly_gdf = gpd.read_file(POLY_SRC)

geom = unary_union(poly_gdf.geometry).buffer(0)
if isinstance(geom, MultiPolygon):
    geom = max(list(geom.geoms), key=lambda g: g.area)
if isinstance(geom, Polygon):
    geom = Polygon(geom.exterior)

if POLYGON_SHRINK_M != 0:
    shrunk = geom.buffer(-POLYGON_SHRINK_M)
    if not shrunk.is_empty:
        geom = shrunk.buffer(0)

poly = gpd.GeoDataFrame(
    {"id": [1], "name": ["poligono_urbanismo_ipt_outer_real"]},
    geometry=[geom],
    crs=poly_gdf.crs,
)
poly.to_file(OUT_POLY, driver="GPKG")

if grid.crs != poly.crs:
    grid = grid.to_crs(poly.crs)

points = []
values = []

for _, r in grid.iterrows():
    pt = Point(float(r["cx"]), float(r["cy"]))
    z = float(r["z_terrain_m"])
    ztot = float(r["z_total_m"])

    if np.isfinite(z) and z > 0:
        points.append([pt.x, pt.y])
        values.append(z)

points = np.asarray(points, dtype=float)
values = np.asarray(values, dtype=float)

print("Amostras válidas:", len(points))
print("z min/max:", float(values.min()), float(values.max()))
print("Polígono bounds:", poly.total_bounds)

rbf = RBFInterpolator(
    points,
    values,
    kernel="thin_plate_spline",
    smoothing=1.0,
)

minx, miny, maxx, maxy = poly.total_bounds
x = np.linspace(minx, maxx, NX)
y = np.linspace(miny, maxy, NY)
X, Y = np.meshgrid(x, y)

query = np.column_stack([X.ravel(), Y.ravel()])
Z = rbf(query).reshape(NY, NX)
Z = gaussian_filter(Z, sigma=SMOOTH_SIGMA)
Z[Z < 0] = 0

mask = np.zeros((NY, NX), dtype=bool)
for rr in range(NY):
    for cc in range(NX):
        mask[rr, cc] = geom.contains(Point(X[rr, cc], Y[rr, cc]))

Z_masked = Z.copy()
Z_masked[~mask] = np.nan

np.savez_compressed(OUT_SURFACE, x=x, y=y, z=Z_masked)

zmin = np.nanmin(Z_masked)
zmax = np.nanmax(Z_masked)
levels = np.arange(np.ceil(zmin / INTERVAL_M) * INTERVAL_M, zmax + INTERVAL_M, INTERVAL_M)

print("Surface min/max:", float(zmin), float(zmax))
print("Levels:", levels.tolist())

fig, ax = plt.subplots()
cs = ax.contour(X, Y, Z, levels=levels)
plt.close(fig)

features = []

for level, segments in zip(cs.levels, cs.allsegs):
    for coords in segments:
        if len(coords) < 8:
            continue

        line = LineString(coords).simplify(1.0, preserve_topology=True)

        if line.is_empty:
            continue

        # mantém apenas linhas cujo centro cai no polígono externo
        if not geom.contains(line.interpolate(0.5, normalized=True)):
            continue

        features.append({
            "type": "Feature",
            "properties": {
                "elevation": float(level),
                "source": "RBF_REAL_CX_CY_Z_TERRAIN",
            },
            "geometry": mapping(line),
        })

geojson = {"type": "FeatureCollection", "features": features}
OUT_GEOJSON.write_text(json.dumps(geojson), encoding="utf-8")

print("========================================")
print("OUT_POLY:", OUT_POLY)
print("OUT_GEOJSON:", OUT_GEOJSON)
print("OUT_SURFACE:", OUT_SURFACE)
print("features:", len(features))
print("========================================")
