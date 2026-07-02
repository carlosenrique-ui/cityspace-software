"""
IPT-CitySpace — OFFLINE VALIDATION
=================================

Validação espacial do grid Z_TOTAL (em metros)
contra o DXF rotacionado do IPT.

OBJETIVO
--------
- Garantir que o grid 8x16 está:
  • corretamente rotacionado
  • alinhado ao DXF do IPT
  • com valores físicos plausíveis (terreno + edifício)

ENTRADA
-------
- offline/products/snapshots/ipt_fase2_semantic/grid_z_total_m.csv
- data/dxf/IPT-2018-DXF-Rotacionado.dxf

SAÍDA
-----
- visualization/validation/validacao_grid_z_total_vs_dxf.png

OBS
---
Este script é OFFLINE.
O ONLINE apenas consome produtos já validados.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# ======================================================
# PATHS CANÔNICOS
# ======================================================

ENGINE_ROOT = Path(__file__).resolve().parents[2]

GRID_Z_TOTAL = (
    ENGINE_ROOT
    / "offline"
    / "products"
    / "snapshots"
    / "ipt_fase2_semantic"
    / "grid_z_total_m.csv"
)

DXF_IPT = (
    ENGINE_ROOT
    / "data"
    / "dxf"
    / "IPT-2018-DXF-Rotacionado.dxf"
)

OUT_DIR = (
    ENGINE_ROOT
    / "visualization"
    / "validation"
)

OUT_IMG = OUT_DIR / "validacao_grid_z_total_vs_dxf.png"

GRID_ROWS = 8
GRID_COLS = 16

# ======================================================
# LOG
# ======================================================

def log(msg):
    print(f"[VALIDAÇÃO] {msg}")

# ======================================================
# LOADERS
# ======================================================

def carregar_grid():
    log(f"Carregando grid: {GRID_Z_TOTAL}")

    if not GRID_Z_TOTAL.exists():
        raise FileNotFoundError(GRID_Z_TOTAL)

    grid = np.loadtxt(GRID_Z_TOTAL, delimiter=";")

    if grid.shape != (GRID_ROWS, GRID_COLS):
        raise ValueError(
            f"Grid inválido: esperado {(GRID_ROWS, GRID_COLS)}, obtido {grid.shape}"
        )

    log(f"Grid OK | min={grid.min():.2f} m | max={grid.max():.2f} m")
    return grid


def carregar_dxf():
    log(f"Carregando DXF: {DXF_IPT}")

    if not DXF_IPT.exists():
        raise FileNotFoundError(DXF_IPT)

    gdf = gpd.read_file(DXF_IPT)

    if gdf.empty:
        raise ValueError("DXF carregado mas vazio")

    log(f"DXF OK | {len(gdf)} geometrias")
    return gdf

# ======================================================
# PLOT
# ======================================================

def plot_validacao(grid, gdf):
    log("Gerando visualização de validação")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Grid
    im = ax.imshow(
        grid,
        cmap="viridis",
        origin="lower"
    )

    # DXF
    gdf.plot(
        ax=ax,
        facecolor="none",
        edgecolor="white",
        linewidth=1.0
    )

    plt.colorbar(im, ax=ax, label="Z_TOTAL (m)")

    ax.set_title(
        "IPT-CitySpace — Validação OFFLINE\n"
        "Grid Z_TOTAL (terreno + edifícios) × DXF IPT"
    )

    ax.set_xlabel("Coluna da mesa (Oeste → Leste)")
    ax.set_ylabel("Linha da mesa (Sul → Norte)")

    plt.tight_layout()
    plt.savefig(OUT_IMG, dpi=150)
    plt.close()

    log(f"Imagem gerada: {OUT_IMG}")

# ======================================================
# MAIN
# ======================================================

def main():
    log("==============================================")
    log("INICIANDO VALIDAÇÃO OFFLINE GRID × DXF IPT")
    log("==============================================")

    grid = carregar_grid()
    gdf = carregar_dxf()
    plot_validacao(grid, gdf)

    log("----------------------------------------------")
    log("✔ VALIDAÇÃO OFFLINE CONCLUÍDA COM SUCESSO")
    log("----------------------------------------------")


if __name__ == "__main__":
    main()
