"""
CitySpace System Paths
Centralized path configuration for the engine
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

from offline.config.system_parameters import GRID_NAME

# =========================================
# PRODUCTS
# =========================================

SCIENTIFIC_PRODUCTS = BASE / "offline/products/scientific"

# grid
GRID_GPKG = f"grid_{GRID_NAME}_metric.gpkg"
GRID_PATH = SCIENTIFIC_PRODUCTS / GRID_GPKG

# metrics
GRID_METRICS_CSV = SCIENTIFIC_PRODUCTS / "grid_metrics.csv"
GRID_METRICS_UTM_CSV = SCIENTIFIC_PRODUCTS / "grid_metrics_utm.csv"

# building heights
PIN_HEIGHTS_CSV = SCIENTIFIC_PRODUCTS / "pin_heights.csv"

# =========================================
# RASTERS
# =========================================

DSM_LOCAL = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"
DTM_LOCAL = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"

DSM_CLIP = BASE / "offline/data/processed/dsm/IPT_2018_DSM_CLIP.tif"
DTM_CLIP = BASE / "offline/data/processed/dtm/IPT_2018_DTM_CLIP.tif"

HEIGHT = BASE / "offline/data/processed/height/HEIGHT.tif"
HEIGHT_TOTAL = BASE / "offline/data/processed/height/HEIGHT_TOTAL.tif"

# =========================================
# VECTOR DATA
# =========================================

BUILDINGS_VECTOR = BASE / "offline/products/scientific/buildings_scientific_rotated.gpkg"
URBAN_ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"