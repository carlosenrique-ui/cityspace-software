from offline.config.system_parameters import ROTATION_DEG
import geopandas as gpd
from shapely.affinity import rotate, translate
from pathlib import Path

print("========================================")
print("STEP 05 – APPLY SCIENTIFIC ROTATION")
print("========================================")

BASE = Path("offline/products/scientific")

IN_PATH  = BASE / "grid_contours_clean.gpkg"
OUT_PATH = BASE / "grid_contours_rotated_scientific.gpkg"

ANGLE = ROTATION_DEG

if not IN_PATH.exists():
    raise Exception(f"❌ Input não encontrado: {IN_PATH}")

gdf = gpd.read_file(IN_PATH, engine="pyogrio")

print("Loaded:", gdf.shape)

# =========================================
# CENTRO GLOBAL (robusto)
# =========================================
centroid = gdf.geometry.union_all().centroid
cx, cy = centroid.x, centroid.y

print("Centro:", cx, cy)
print("Rotação:", ANGLE)

# =========================================
# ROTATION
# =========================================
gdf["geometry"] = gdf.geometry.apply(
    lambda g: rotate(g, ANGLE, origin=(cx, cy), use_radians=False)
)

# =========================================
# TRANSLATE → ORIGEM (0,0)
# =========================================
minx, miny, maxx, maxy = gdf.total_bounds

print("Bounds antes:", minx, miny, maxx, maxy)

gdf["geometry"] = gdf.geometry.apply(
    lambda g: translate(g, xoff=-minx, yoff=-miny)
)

# =========================================
# VALIDATION
# =========================================
minx2, miny2, maxx2, maxy2 = gdf.total_bounds

print("Bounds depois:", minx2, miny2, maxx2, maxy2)

# =========================================
# SAVE
# =========================================
gdf.to_file(OUT_PATH, driver="GPKG", engine="pyogrio")

print("========================================")
print("✅ OUTPUT:", OUT_PATH)
print("========================================")

