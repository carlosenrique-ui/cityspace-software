#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL — DEBUG V4 (ORIENTAÇÃO FINAL DA MESA)
# IPT CitySpace
# ==========================================================
# Correção aplicada:
# - Rotação 180° em torno de eixo paralelo a X
#   => FLIP EM Y (linhas)
# - Mantém cores e tempos físicos corretos
# ==========================================================

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import imageio.v2 as imageio
from matplotlib.patches import Rectangle

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

GIF_PATH = OUT_DIR / "mesa_virtual_debug_v4.gif"

# ----------------------------------------------------------
# CONFIGURAÇÃO DA MESA
# ----------------------------------------------------------

ROWS = 8
COLS = 16
FPS = 6

MIN_FRAMES = 1
MAX_FRAMES = 8

# ----------------------------------------------------------
# LOAD GRID (Z TOTAL REAL)
# ----------------------------------------------------------

print("[LOAD] Grid Z_total_real")
grid_raw = np.loadtxt(GRID_PATH, delimiter=";")
assert grid_raw.shape == (ROWS, COLS)

# 👉 CORREÇÃO DEFINITIVA DE ORIENTAÇÃO
grid = grid_raw[::-1, :]

Z_MIN = np.nanmin(grid)
Z_MAX = np.nanmax(grid)

print(f"[INFO] Altura mínima: {Z_MIN:.3f} m")
print(f"[INFO] Altura máxima: {Z_MAX:.3f} m")

# ----------------------------------------------------------
# LOAD DXF (mantido)
# ----------------------------------------------------------

print("[LOAD] DXF IPT")
gdf = gpd.read_file(DXF_PATH)
minx, miny, maxx, maxy = gdf.total_bounds

def norm_x(x):
    return (x - minx) / (maxx - minx) * COLS

def norm_y(y):
    return (maxy - y) / (maxy - miny) * ROWS

# ----------------------------------------------------------
# ZIG-ZAG (OK)
# ----------------------------------------------------------

trajetoria = []
for c in range(COLS):
    if c % 2 == 0:
        for r in range(ROWS):
            trajetoria.append((r, c))
    else:
        for r in range(ROWS - 1, -1, -1):
            trajetoria.append((r, c))

# ----------------------------------------------------------
# ALTURA → TEMPO FÍSICO
# ----------------------------------------------------------

def frames_por_altura(z):
    f = (z - Z_MIN) / (Z_MAX - Z_MIN) if Z_MAX > Z_MIN else 0
    return int(MIN_FRAMES + f * (MAX_FRAMES - MIN_FRAMES))

# ----------------------------------------------------------
# RENDER
# ----------------------------------------------------------

frames = []
estado = np.zeros_like(grid)

print("[RENDER] Simulação física da mesa...")

for (r, c) in trajetoria:

    estado[r, c] = grid[r, c]
    z = grid[r, c]
    n_frames = frames_por_altura(z)

    for _ in range(n_frames):

        fig, ax = plt.subplots(figsize=(10, 5))

        im = ax.imshow(
            estado,
            cmap="viridis",
            vmin=Z_MIN,
            vmax=Z_MAX,
            origin="upper"
        )

        ax.set_xticks(range(COLS))
        ax.set_yticks(range(ROWS))
        ax.grid(color="white", linewidth=0.5, alpha=0.4)

        ax.set_xlabel("Coluna do pino (Oeste → Leste)")
        ax.set_ylabel("Linha do pino (Norte → Sul)")

        # DXF
        for geom in gdf.geometry:
            if geom.geom_type == "Polygon":
                xs, ys = geom.exterior.xy
                ax.plot(
                    [norm_x(x) for x in xs],
                    [norm_y(y) for y in ys],
                    color="red",
                    linewidth=1.1,
                    alpha=0.4
                )

        # QUADRADO BRANCO
        ax.add_patch(
            Rectangle(
                (c - 0.5, r - 0.5),
                1, 1,
                fill=False,
                edgecolor="white",
                linewidth=2
            )
        )

        ax.set_title(
            f"Mesa Virtual 8×16 — Estado Acumulado\n"
            f"Altura = {z:.3f} m | Frames = {n_frames}",
            fontsize=11
        )

        cbar = plt.colorbar(im, ax=ax, fraction=0.046)
        cbar.set_label("Altura do pino (m) — equivalente real IPT")

        # Captura ARGB → RGB
        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()
        argb = np.frombuffer(
            fig.canvas.tostring_argb(),
            dtype=np.uint8
        ).reshape((h, w, 4))

        rgb = np.zeros((h, w, 3), dtype=np.uint8)
        rgb[..., 0] = argb[..., 1]
        rgb[..., 1] = argb[..., 2]
        rgb[..., 2] = argb[..., 3]

        frames.append(rgb)
        plt.close(fig)

# ----------------------------------------------------------
# SAVE GIF
# ----------------------------------------------------------

print("[SAVE] Gerando GIF...")
imageio.mimsave(GIF_PATH, frames, fps=FPS)

print("[OK] GIF gerado:")
print(GIF_PATH)
