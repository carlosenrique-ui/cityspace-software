"""
OFFLINE TEST — GERAÇÃO DE CURVAS DE NÍVEL
========================================

Teste isolado da geração da layer de curvas de nível (PNG),
sem rodar o runner OFFLINE completo.
"""

import sys
from pathlib import Path
import numpy as np

# ---------------------------------------------------------
# GARANTE QUE O ROOT DO PROJETO ESTEJA NO PYTHONPATH
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------
# IMPORT CORRETO: MÓDULO GEO (PRODUTOR REAL DA CURVA)
# ---------------------------------------------------------

from offline.geo.contours.csv_to_contours import (
    csv_to_contour_png
)

# ---------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------

SNAPSHOT_DIR = (
    PROJECT_ROOT
    / "offline"
    / "products"
    / "snapshots"
    / "1cm_rotated"
)

GRID_METROS_CSV = SNAPSHOT_DIR / "grid_metros.csv"
OUTPUT_PNG = SNAPSHOT_DIR / "layer_curvas_TESTE.png"

# ---------------------------------------------------------
# TESTE
# ---------------------------------------------------------

def main():

    print("\n[TEST OFFLINE] Geração de curvas de nível\n")

    if not GRID_METROS_CSV.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {GRID_METROS_CSV}"
        )

    print("✔ grid_metros.csv encontrado")

    grid_m = np.loadtxt(GRID_METROS_CSV, delimiter=";")
    print(
        f"✔ Grid carregado | shape={grid_m.shape} "
        f"min={grid_m.min():.4f} max={grid_m.max():.4f}"
    )

    # Gera SOMENTE a layer de curvas
    csv_to_contour_png(
        csv_path=GRID_METROS_CSV,
        output_png=OUTPUT_PNG
    )

    if OUTPUT_PNG.exists():
        print(f"✔ Layer gerada com sucesso: {OUTPUT_PNG.name}")
    else:
        raise RuntimeError("❌ Falha na geração da layer PNG")

    print("\n[TEST OFFLINE] OK\n")


if __name__ == "__main__":
    main()
