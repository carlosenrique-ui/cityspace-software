"""
IPT-CitySpace
Export grid_z_total_m.csv to Excel

Gera planilha Excel com as alturas totais da mesa.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# -------------------------------------------------
# ROOT
# -------------------------------------------------

ENGINE_ROOT = Path(__file__).resolve().parents[2]

# -------------------------------------------------
# INPUT
# -------------------------------------------------

CSV_PATH = ENGINE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/grid_z_total_m.csv"

# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

OUT_DIR = ENGINE_ROOT / "offline/products/scientific"
OUT_DIR.mkdir(exist_ok=True)

OUT_XLSX = OUT_DIR / "grid_z_total_m.xlsx"

# -------------------------------------------------

def main():

    print("\n=================================")
    print("CITYSPACE – EXPORT ALTURAS EXCEL")
    print("=================================")

    if not CSV_PATH.exists():
        raise RuntimeError(f"Arquivo não encontrado:\n{CSV_PATH}")

    # carregar matriz
    grid = np.loadtxt(CSV_PATH, delimiter=";")

    rows, cols = grid.shape

    print("Grid detectado:", rows, "x", cols)

    # criar dataframe
    df = pd.DataFrame(grid)

    df.index.name = "row"
    df.columns = [f"col_{i}" for i in range(cols)]

    print("\nSalvando Excel:")

    df.to_excel(OUT_XLSX)

    print(OUT_XLSX)

# -------------------------------------------------

if __name__ == "__main__":
    main()