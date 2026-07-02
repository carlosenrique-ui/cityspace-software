from pathlib import Path

path = Path("config/system_paths.py")

append_block = """

# =========================================
# FIX GRID PATH (CORRECT CONFIG)
# =========================================
from pathlib import Path

BASE_DIR = Path("offline/products/scientific")
GRID_GPKG = BASE_DIR / "grid_8x16_metric.gpkg"
"""

with open(path, "a") as f:
    f.write(append_block)

print("✅ GRID_GPKG gravado com sucesso")
