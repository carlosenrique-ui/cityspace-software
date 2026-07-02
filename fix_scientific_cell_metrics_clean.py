from pathlib import Path

file = Path("offline/scientific_cell_metrics_utm.py")
code = file.read_text()

# 🔥 BLOCO CORRETO
correct_block = '''
import pyogrio
from pathlib import Path

BASE = Path("offline/products/scientific")
GRID_PATH = BASE / "grid_8x16_metric.gpkg"

def main():
    print("[1/6] Lendo grid científico...")

    gdf = pyogrio.read_dataframe(GRID_PATH)

    print("Cells:", len(gdf))
'''

# 🔥 substitui tudo antes do main antigo
import re
code = re.sub(
    r"(def main\(\):[\s\S]*?print\(\"Cells:\", len\(gdf\)\))",
    correct_block.strip(),
    code
)

file.write_text(code)

print("✅ scientific_cell_metrics_utm RECONSTRUÍDO")
