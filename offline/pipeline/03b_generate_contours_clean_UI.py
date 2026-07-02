# =========================================
# IPT-CITYSPACE — CURVAS DTM LIMPAS PARA UI
# =========================================

from pathlib import Path
import geopandas as gpd

# =========================================
# PATHS
# =========================================

BASE = Path(__file__).resolve().parents[2]
PROJECT = BASE.parent

INPUT = PROJECT / "offline/products/terrain/curvas_nivel_terreno_suavizadas_UI.geojson"
OUTPUT = BASE / "offline/products/scientific/curvas_ui_clean_2m.gpkg"

# =========================================
# LOAD
# =========================================

gdf = gpd.read_file(INPUT)

print("INPUT:", INPUT)
print("rows original:", len(gdf))

# =========================================
# 1) REMOVER COTA ZERO
# =========================================

gdf = gdf[gdf["elevation"] > 0]

# =========================================
# 2) INTERVALO DE 2m
# =========================================

gdf = gdf[gdf["elevation"] % 2 == 0]

print("rows após filtro 2m:", len(gdf))

# =========================================
# 3) CLIP ESPACIAL (REMOVE LIXO LATERAL)
# =========================================

minx, miny, maxx, maxy = gdf.total_bounds

# reduz bounding box em 5% (remove bordas ruins)
dx = (maxx - minx) * 0.05
dy = (maxy - miny) * 0.05

from shapely.geometry import box

clip_geom = box(
    minx + dx,
    miny + dy,
    maxx - dx,
    maxy - dy
)

clip_gdf = gpd.GeoDataFrame(
    geometry=[clip_geom],
    crs=gdf.crs
)

gdf = gpd.clip(gdf, clip_gdf)

print("rows após clip:", len(gdf))

# =========================================
# 4) SUAVIZAÇÃO (SIMPLIFY)
# =========================================

gdf["geometry"] = gdf.geometry.simplify(
    tolerance=0.5,  # ajuste fino
    preserve_topology=True
)

print("rows final:", len(gdf))

# =========================================
# SAVE
# =========================================

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
gdf.to_file(OUTPUT)

print("========================================")
print("OUTPUT:", OUTPUT)
print("========================================")
