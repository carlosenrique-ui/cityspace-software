#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL — DEBUG V1
# IPT CitySpace
# ==========================================================
# Objetivo:
# - Validar orientação da mesa
# - Validar DXF sem inversão
# - Validar Z_total_real (terreno + pino)
# - SALVAR IMAGEM (WSL-friendly)
# ==========================================================

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

ENGINE_ROOT = Path(__file__).resolve().parents[3]

GRID_PATH = (
    ENGINE_ROOT
    / "offline"
    / "products"
    / "snapshots"
    / "ipt_fase2_semantic"
    / "grid_z_total_m.csv"
)

DXF_PATH = (
    ENGINE_ROOT
    / "offline"
    / "products"
    / "fase2"
    / "dxf"
    / "IPT-2018-DXF-Rotacionado.dxf"
)

OUT_DIR = ENGINE_ROOT / "online" / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_IMG = OUT_DIR / "mesa_virtual_debug_v1.png"

# ----------------------------------------------------------
# CONFIGURAÇÃO DA MESA
# ----------------------------------------------------------

ROWS = 8
COLS = 16

# ----------------------------------------------------------
# LOAD GRID (Z TOTAL REAL)
# ----------------------------------------------------------

print("[LOAD] Grid Z_total_real")
grid = np.loadtxt(GRID_PATH, delimiter=";")

assert grid.shape == (ROWS, COLS), "Grid não é 8x16"

Z_MIN = np.nanmin(grid)
Z_MAX = np.nanmax(grid)

print(f"[INFO] Altura mínima: {Z_MIN:.3f} m")
print(f"[INFO] Altura máxima: {Z_MAX:.3f} m")

# ----------------------------------------------------------
# LOAD DXF (SEM INVERSÃO)
# ----------------------------------------------------------

print("[LOAD] DXF IPT")
gdf = gpd.read_file(DXF_PATH)

minx, miny, maxx, maxy = gdf.total_bounds

def norm_x(x):
    return (x - minx) / (maxx - minx) * COLS

def norm_y(y):
    return (y - miny) / (maxy - miny) * ROWS

# ----------------------------------------------------------
# RENDER ESTÁTICO → PNG
# ----------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 5))

im = ax.imshow(
    grid,
    cmap="inferno",
    vmin=Z_MIN,
    vmax=Z_MAX,
    origin="upper"
)

ax.set_xticks(range(COLS))
ax.set_yticks(range(ROWS))
ax.grid(color="white", linewidth=0.5, alpha=0.4)

ax.set_xlabel("Colunas da mesa (X)")
ax.set_ylabel("Linhas da mesa (Y)")

# OVERLAY DXF
for geom in gdf.geometry:
    if geom.geom_type == "Polygon":
        xs, ys = geom.exterior.xy
        ax.plot(
            [norm_x(x) for x in xs],
            [norm_y(y) for y in ys],
            color="red",
            linewidth=1.2,
            alpha=0.6
        )

cbar = plt.colorbar(im, ax=ax, fraction=0.046)
cbar.set_label("Altura total real (terreno + pino) [m]")

ax.set_title("Mesa Virtual IPT — DEBUG V1")

plt.tight_layout()
plt.savefig(OUT_IMG, dpi=150)
plt.close(fig)

print("[OK] Imagem gerada:")
print(OUT_IMG)
