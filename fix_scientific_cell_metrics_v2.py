from pathlib import Path

file = Path("offline/scientific_cell_metrics_utm.py")
code = file.read_text()

# garantir import correto
if "import pyogrio" not in code:
    code = "import pyogrio\n" + code

# garantir GRID_PATH definido
if "GRID_PATH" not in code:
    code = code.replace(
        "def main():",
        """GRID_PATH = "offline/products/scientific/grid_8x16_metric.gpkg"

def main():"""
    )

# garantir leitura correta do grid
if "read_dataframe" not in code:
    code = code.replace(
        "print(\"[1/6] Lendo grid científico...\")",
        """print("[1/6] Lendo grid científico...")
    gdf = pyogrio.read_dataframe(GRID_PATH)"""
    )

file.write_text(code)

print("✅ scientific_cell_metrics_utm FIX FINAL aplicado")
