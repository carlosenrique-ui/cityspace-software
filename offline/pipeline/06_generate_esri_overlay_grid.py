from pathlib import Path
import requests
import geopandas as gpd
from pyproj import Transformer

BASE = Path(__file__).resolve().parents[2]

GRID = BASE / "offline/products/scientific/grid_8x16_enriched.gpkg"
OUT = BASE / "offline/products/snapshots/ipt_fase2_semantic/esri_overlay_grid.png"

OUT.parent.mkdir(parents=True, exist_ok=True)

gdf = gpd.read_file(GRID)

xmin, ymin, xmax, ymax = gdf.total_bounds

# buffer leve
dx = xmax - xmin
dy = ymax - ymin
xmin -= dx * 0.10
xmax += dx * 0.10
ymin -= dy * 0.10
ymax += dy * 0.10

# =========================================
# CONVERSÃO UTM → WGS84
# =========================================

transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)

lon_min, lat_min = transformer.transform(xmin, ymin)
lon_max, lat_max = transformer.transform(xmax, ymax)

# =========================================
# REQUEST ESRI (WGS84)
# =========================================

url = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"

params = {
    "bbox": f"{lon_min},{lat_min},{lon_max},{lat_max}",
    "bboxSR": "4326",
    "imageSR": "4326",
    "size": "1600,900",
    "format": "png",
    "transparent": "false",
    "f": "image",
}

print("========================================")
print("ESRI DOWNLOAD (WGS84)")
print("OUT:", OUT)
print("BBOX:", params["bbox"])
print("========================================")

r = requests.get(url, params=params, timeout=60)
r.raise_for_status()

OUT.write_bytes(r.content)

print("OK:", OUT)
print("bytes:", OUT.stat().st_size)
