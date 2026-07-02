from pathlib import Path

file = Path("offline/scientific_cell_metrics_utm.py")

code = file.read_text()

# substitui uso errado de GRID_PATH
code = code.replace(
    'GRID_PATH',
    '"offline/products/scientific/grid_8x16_metric.gpkg"'
)

file.write_text(code)

print("✅ scientific_cell_metrics_utm corrigido para usar GPKG")
