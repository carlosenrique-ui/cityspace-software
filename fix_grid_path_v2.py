from pathlib import Path

path = Path("config/system_paths.py")

append_block = """

# =========================================
# FIX GRID METRICS CSV
# =========================================
from pathlib import Path

BASE_DIR = Path("offline/products/scientific")

GRID_METRICS_UTM_CSV = BASE_DIR / "grid_metrics_utm.csv"
"""

with open(path, "a") as f:
    f.write(append_block)

print("✅ GRID_METRICS_UTM_CSV adicionado")
