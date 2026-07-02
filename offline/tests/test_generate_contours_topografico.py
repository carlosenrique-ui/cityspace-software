"""
OFFLINE TEST — CURVAS DE NÍVEL TOPOGRÁFICAS (INFORMATIVO)
========================================================

Gera uma layer de curvas de nível:
- referenciadas ao terreno (0.00 m)
- suavizadas
- com espaçamento legível
- fundo transparente

NÃO representa controle físico dos pinos.
É apenas produto visual / informativo.
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ---------------------------------------------------------
# PYTHONPATH FIX
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
OUTPUT_PNG = SNAPSHOT_DIR / "layer_curvas_TOPOGRAFICO.png"

CELL_SIZE_CM = 1.0
PX_PER_CM = 120

# Curvas mais espaçadas (legibilidade)
EQUIDISTANCIA_M = 0.01   # 1 cm
SIGMA_SUAVIZACAO = 1.0   # suavização gaussiana

# ---------------------------------------------------------
# TESTE
# ---------------------------------------------------------

def main():

    print("\n[TEST OFFLINE] Curvas de nível topográficas\n")

    if not GRID_METROS_CSV.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {GRID_METROS_CSV}"
        )

    z = np.loadtxt(GRID_METROS_CSV, delimiter=";")

    print(
        f"✔ Grid carregado | shape={z.shape} "
        f"min={z.min():.4f} max={z.max():.4f}"
    )

    # -----------------------------------------------------
    # 1. REFERÊNCIA AO TERRENO (0.00 m)
    # -----------------------------------------------------

    z_rel = z - z.min()

    print(
        f"✔ Referência ao terreno | "
        f"min={z_rel.min():.4f} max={z_rel.max():.4f}"
    )

    # -----------------------------------------------------
    # 2. SUAVIZAÇÃO
    # -----------------------------------------------------

    z_smooth = gaussian_filter(z_rel, sigma=SIGMA_SUAVIZACAO)

    # -----------------------------------------------------
    # 3. GRADE ESPACIAL
    # -----------------------------------------------------

    nrows, ncols = z.shape
    x = np.arange(0.5, ncols + 0.5) * CELL_SIZE_CM
    y = np.arange(0.5, nrows + 0.5) * CELL_SIZE_CM
    X, Y = np.meshgrid(x, y)

    # -----------------------------------------------------
    # 4. CURVAS DE NÍVEL
    # -----------------------------------------------------

    levels = np.arange(
        0,
        z_smooth.max() + EQUIDISTANCIA_M,
        EQUIDISTANCIA_M
    )

    width_cm = ncols * CELL_SIZE_CM
    height_cm = nrows * CELL_SIZE_CM

    fig = plt.figure(
        figsize=(width_cm / 2.54, height_cm / 2.54)
    )
    ax = plt.axes([0, 0, 1, 1])
    ax.set_axis_off()

    cs = ax.contour(
        X, Y, z_smooth,
        levels=levels,
        colors="black",
        linewidths=1
    )

    # Rótulos menos frequentes
    ax.clabel(
        cs,
        cs.levels[::2],   # rotula uma curva sim / uma não
        inline=True,
        fontsize=7,
        fmt="%.2f m"
    )

    # Sistema da mesa
    ax.invert_yaxis()
    ax.set_xlim(0, width_cm)
    ax.set_ylim(height_cm, 0)
    ax.set_aspect("equal")

    plt.savefig(
        OUTPUT_PNG,
        dpi=PX_PER_CM * 2.54,
        transparent=True
    )
    plt.close(fig)

    print(f"✔ Layer topográfica gerada: {OUTPUT_PNG.name}")
    print("\n[TEST OFFLINE] OK\n")


if __name__ == "__main__":
    main()
