import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =============================
# INPUTS (CIENTÍFICO)
# =============================
DTM_LOCAL = "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"
DSM_LOCAL = "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"

# =============================
# OUTPUTS
# =============================
GRID_PATH = os.path.join(BASE_DIR, "offline/products/scientific/grid.npy")

CSV_METRICS = os.path.join(
    BASE_DIR,
    "offline/products/scientific/grid_metrics_utm.csv"
)

CSV_SEMANTIC = os.path.join(
    BASE_DIR,
    "offline/products/semantic/grid_semantic.csv"
)

ACTUATOR_PLAN = os.path.join(
    BASE_DIR,
    "products/final/actuator_plan.json"
)

# =========================================
# FIX GRID PATH (CORRECT CONFIG)
# =========================================
from pathlib import Path

BASE_DIR = Path("offline/products/scientific")
GRID_GPKG = BASE_DIR / "grid_8x16_metric.gpkg"


# =========================================
# FIX GRID METRICS CSV
# =========================================
from pathlib import Path

BASE_DIR = Path("offline/products/scientific")

GRID_METRICS_UTM_CSV = BASE_DIR / "grid_metrics_utm.csv"
