from pathlib import Path
import numpy as np
import geopandas as gpd
import requests
from PIL import Image
from io import BytesIO
from pyproj import Transformer

BASE = Path(__file__).resolve().parents[2]

GRID = BASE / "offline/products/scientific/grid_8x16_enriched.gpkg"
OUT = BASE / "offline/products/snapshots/ipt_fase2_semantic/esri_overlay_grid.png"

ROWS = 8
COLS = 16

print("========================================")
print("ESRI → GRID (VERSÃO FUNCIONAL)")
print("========================================")

gdf = gpd.read_file(GRID)

# =========================================
# LIMITES UTM
# =========================================

xmin, ymin, xmax, ymax = gdf.total_bounds

# buffer
dx = xmax - xmin
dy = ymax - ymin
xmin -= dx * 0.15
xmax += dx * 0.15
ymin -= dy * 0.15
ymax += dy * 0.15

# =========================================
# UTM → WEB MERCATOR (ESRI)
# =========================================

transformer = Transformer.from_crs("EPSG:31983", "EPSG:3857", always_xy=True)

mxmin, mymin = transformer.transform(xmin, ymin)
mxmax, mymax = transformer.transform(xmax, ymax)

# =========================================
# DOWNLOAD ESRI
# =========================================

url = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"

params = {
    "bbox": f"{mxmin},{mymin},{mxmax},{mymax}",
    "bboxSR": "3857",
    "imageSR": "3857",
    "size": "2000,1000",
    "format": "png",
    "f": "image"
}

r = requests.get(url, params=params, timeout=60)
r.raise_for_status()

img = Image.open(BytesIO(r.content)).convert("RGB")

# =========================================
# REDIMENSIONAR PARA GRID (SIMPLES)
# =========================================

img_resized = img.resize((COLS * 100, ROWS * 100), Image.BILINEAR)

OUT.parent.mkdir(parents=True, exist_ok=True)
img_resized.save(OUT)

print("OK:", OUT)
