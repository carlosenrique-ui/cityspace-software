# =========================================
# IPT-CITYSPACE — CONTOURS DIRETO DO DTM REAL
# =========================================

from pathlib import Path
import geopandas as gpd
import subprocess

# =========================================
# PATHS
# =========================================

BASE = Path(__file__).resolve().parents[2]

DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"

OUTPUT = BASE / "offline/products/scientific/curvas_dtm_true_2m.gpkg"

# =========================================
# CHECK
# =========================================

if not DTM.exists():
    raise FileNotFoundError(f"DTM não encontrado: {DTM}")

print("DTM:", DTM)

# =========================================
# GDAL CONTOUR
# =========================================

cmd = [
    "gdal_contour",
    "-i", "2",
    "-a", "elevation",
    str(DTM),
    str(OUTPUT)
]

print("Executando:", " ".join(cmd))
subprocess.run(cmd, check=True)

# =========================================
# LOAD RESULT
# =========================================

gdf = gpd.read_file(OUTPUT)

print("rows bruto:", len(gdf))

# =========================================
# REMOVER COTA ZERO
# =========================================

gdf = gdf[gdf["elevation"] > 0]

# =========================================
# SUAVIZAÇÃO LEVE
# =========================================

gdf["geometry"] = gdf.geometry.simplify(
    tolerance=0.3,
    preserve_topology=True
)

print("rows final:", len(gdf))

# =========================================
# SAVE FINAL
# =========================================

gdf.to_file(OUTPUT)

print("========================================")
print("OUTPUT:", OUTPUT)
print("========================================")
