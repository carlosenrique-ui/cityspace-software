from pathlib import Path

file = Path("offline/scientific_cell_metrics_utm.py")
code = file.read_text()

# 1. remover import quebrado
lines = code.split("\n")
new_lines = []

for line in lines:
    if "grid_8x16_metric.gpkg" in line:
        continue
    new_lines.append(line)

code = "\n".join(new_lines)

# 2. garantir GRID_PATH correto
if "GRID_PATH" not in code:
    code = code.replace(
        "def main():",
        """GRID_PATH = "offline/products/scientific/grid_8x16_metric.gpkg"

def main():"""
    )

file.write_text(code)

print("✅ scientific_cell_metrics_utm corrigido")
