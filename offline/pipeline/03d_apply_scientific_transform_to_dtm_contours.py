from pathlib import Path
import geopandas as gpd
from shapely.affinity import rotate, translate, scale
from shapely.geometry import box

# =========================================
# PATHS
# =========================================

BASE = Path(__file__).resolve().parents[2]

INPUT = BASE / "offline/products/scientific/curvas_dtm_true_2m.gpkg"
OUTPUT = BASE / "offline/products/scientific/curvas_dtm_rotated_scientific.gpkg"

# =========================================
# LOAD
# =========================================

gdf = gpd.read_file(INPUT, layer="curvas_dtm_true_2m")

print("INPUT:", INPUT)
print("rows:", len(gdf))

# =========================================
# ROTATION PARAM
# =========================================

ROTATION_DEG = 154.63

minx, miny, maxx, maxy = gdf.total_bounds
cx = (minx + maxx) / 2
cy = (miny + maxy) / 2

print("Centro:", cx, cy)

# =========================================
# 1) ROTATE
# =========================================

gdf["geometry"] = gdf.geometry.apply(
    lambda g: rotate(g, ROTATION_DEG, origin=(cx, cy))
)

# =========================================
# 2) TRANSLATE TO ORIGIN
# =========================================

minx, miny, maxx, maxy = gdf.total_bounds

gdf["geometry"] = gdf.geometry.apply(
    lambda g: translate(g, xoff=-minx, yoff=-miny)
)

# =========================================
# 3) RECALCULAR BOUNDS (CRÍTICO)
# =========================================

minx, miny, maxx, maxy = gdf.total_bounds

print("Bounds pós translate:", minx, miny, maxx, maxy)

# =========================================
# 4) FLIP Y CORRETO
# =========================================

gdf["geometry"] = gdf.geometry.apply(
    lambda g: scale(g, xfact=1, yfact=-1, origin=(0, maxy))
)

# =========================================
# 5) CLIP SUAVE (OPCIONAL)
# =========================================

margin_x = (maxx - minx) * 0.02
margin_y = (maxy - miny) * 0.02

clip_geom = box(
    minx + margin_x,
    miny + margin_y,
    maxx - margin_x,
    maxy - margin_y
)

clip_gdf = gpd.GeoDataFrame(geometry=[clip_geom], crs=gdf.crs)

gdf = gpd.clip(gdf, clip_gdf)

print("rows após clean:", len(gdf))

# =========================================
# SAVE
# =========================================

gdf.to_file(OUTPUT)

print("========================================")
print("OUTPUT:", OUTPUT)
print("========================================")
