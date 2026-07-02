#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL IPT — 2D / 2.5D INTEGRADA
#
# Base geográfica:
#   - DSM em EPSG:4326
#   - Norte geográfico = eixo +latitude
#   - Rotação trigonométrica aplicada = 154.63°
#
# Funcionalidades:
#   - IPT (DXF) como fundo, com ruas
#   - Scanner zig-zag por coluna
#   - Célula ativa com borda branca
#   - Cores + legenda (altura)
#   - Tempo por célula proporcional à altura
#   - Títulos por fase histórica
#   - Rosa dos ventos (Norte verdadeiro rotacionado)
#
# Autor: Carlos E. H. Simoes
# ==========================================================

import os
import time
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from shapely.affinity import rotate
from matplotlib.patches import Rectangle, FancyArrow
from math import sin, cos, radians
from datetime import datetime

# ----------------------------------------------------------
# CONFIGURAÇÃO DA MESA
# ----------------------------------------------------------
ROWS, COLS = 8, 16
EXTENT = [0, COLS, ROWS, 0]

# ----------------------------------------------------------
# ARQUIVOS (ajuste se necessário)
# ----------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"
CSV_HEIGHTS = "/mnt/c/IPT-CitySpace-2018/data/output/csv/BMP_1cm_rot_latest.csv"

OUT_DIR = "visualization/gif"
FRAMES_DIR = f"{OUT_DIR}/frames_mesa_ipt"
GIF_PATH = f"{OUT_DIR}/mesa_ipt_2d25_integrada.gif"

os.makedirs(FRAMES_DIR, exist_ok=True)

# ----------------------------------------------------------
# ROTAÇÃO CONSOLIDADA
# ----------------------------------------------------------
ANGLE_DEG = 154.63
theta = radians(ANGLE_DEG)

# Norte original (EPSG:4326)
N_original = np.array([0, 1])

# Norte após rotação
N_rot = np.array([-sin(theta), cos(theta)])

# ----------------------------------------------------------
# VISUAL
# ----------------------------------------------------------
DXF_COLOR = "white"
DXF_ALPHA = 0.85
DXF_LW = 0.8

COLORMAP = "viridis"

# tempos (segundos)
T_MIN = 0.05
T_MAX = 0.25

# ----------------------------------------------------------
# FASES TEMPORAIS
# ----------------------------------------------------------
TEMPORAL_PHASES = [
    (0, 20, "Fase de implantação na USP (1934–1950)"),
    (21, 50, "Fase de expansão do campus (1950–1980)"),
    (51, 90, "Fase de consolidação institucional (1980–2000)"),
    (91, 999, "IPT contemporâneo (2000–hoje)")
]

# ----------------------------------------------------------
def log(msg):
    print(msg)

# ----------------------------------------------------------
def zigzag_path(rows, cols):
    path = []
    for c in range(cols):
        if c % 2 == 0:
            for r in range(rows):
                path.append((r, c))
        else:
            for r in reversed(range(rows)):
                path.append((r, c))
    return path

# ----------------------------------------------------------
def get_phase(idx):
    for a, b, label in TEMPORAL_PHASES:
        if a <= idx <= b:
            return label
    return ""

# ----------------------------------------------------------
def load_heights():
    log("[DATA] Carregando alturas (8x16)")
    if os.path.exists(CSV_HEIGHTS):
        return np.loadtxt(CSV_HEIGHTS, delimiter=";")
    log("[WARN] CSV não encontrado, usando mock")
    return np.random.uniform(0, 30, (ROWS, COLS))

# ----------------------------------------------------------
def load_dxf():
    log("[DXF] Carregando planta IPT")
    gdf = gpd.read_file(DXF_PATH, layer="entities")
    gdf = gdf[gdf.geom_type.isin(["LineString", "MultiLineString"])]

    log(f"[DXF] Aplicando rotação {ANGLE_DEG:.2f}°")
    gdf["geometry"] = gdf["geometry"].apply(
        lambda g: rotate(g, ANGLE_DEG, origin="center", use_radians=False)
    )

    minx, miny, maxx, maxy = gdf.total_bounds

    def normalize(geom):
        x, y = geom.xy
        x = (np.array(x) - minx) / (maxx - minx) * COLS
        y = (np.array(y) - miny) / (maxy - miny) * ROWS
        return type(geom)(zip(x, y))

    gdf["geometry"] = gdf["geometry"].apply(normalize)
    return gdf

# ----------------------------------------------------------
def draw_north(ax):
    cx, cy = COLS - 1.5, 1.5
    scale = 1.2
    ax.add_patch(
        FancyArrow(
            cx, cy,
            N_rot[0] * scale,
            -N_rot[1] * scale,
            width=0.08,
            color="white",
            zorder=20
        )
    )
    ax.text(cx, cy - 0.3, "N", color="white", ha="center", va="top")

# ----------------------------------------------------------
def cell_time(z, zmin, zmax):
    zn = (z - zmin) / (zmax - zmin + 1e-6)
    return T_MIN + zn * (T_MAX - T_MIN)

# ----------------------------------------------------------
def render_frame(grid, gdf, active, idx, heights, zmin, zmax):
    fig, ax = plt.subplots(figsize=(10, 5))

    im = ax.imshow(
        grid,
        cmap=COLORMAP,
        extent=EXTENT,
        origin="upper",
        vmin=zmin,
        vmax=zmax,
        zorder=3
    )

    gdf.plot(ax=ax, color=DXF_COLOR, linewidth=DXF_LW, alpha=DXF_ALPHA, zorder=6)

    r, c = active
    ax.add_patch(Rectangle((c, r), 1, 1, fill=False, edgecolor="white", linewidth=3, zorder=10))

    draw_north(ax)

    plt.colorbar(im, ax=ax, label="Altura (m)")

    ax.set_title(
        f"Mesa Virtual IPT — 2D / 2.5D\n"
        f"{get_phase(idx)}\n"
        f"Célula {idx+1}/{ROWS*COLS}"
    )

    ax.set_xlabel("Eixo X — Sentido Bairro (Av. Escola Politécnica)")
    ax.set_ylabel("Eixo Y — Sentido Campus (USP)")
    ax.set_xlim(0, COLS)
    ax.set_ylim(ROWS, 0)
    ax.grid(alpha=0.2)

    frame = f"{FRAMES_DIR}/frame_{idx:03d}.png"
    plt.tight_layout()
    plt.savefig(frame, dpi=150)
    plt.close()
    return frame

# ----------------------------------------------------------
def main():
    log("=" * 70)
    log("MESA VIRTUAL IPT — EXECUÇÃO INTEGRADA")
    log(f"Início: {datetime.now()}")
    log("=" * 70)

    heights = load_heights()
    zmin, zmax = heights.min(), heights.max()

    gdf = load_dxf()
    path = zigzag_path(ROWS, COLS)

    grid = np.zeros((ROWS, COLS))
    frames = []

    for idx, (r, c) in enumerate(path):
        grid[r, c] = heights[r, c]

        frame = render_frame(grid, gdf, (r, c), idx, heights, zmin, zmax)
        frames.append(frame)

        t = cell_time(heights[r, c], zmin, zmax)
        time.sleep(t)

    log("[GIF] Gerando animação final")
    images = [imageio.imread(f) for f in frames]
    imageio.mimsave(GIF_PATH, images, fps=6)

    log("=" * 70)
    log("FINALIZADO COM SUCESSO")
    log(f"Arquivo: {GIF_PATH}")
    log("=" * 70)

# ----------------------------------------------------------
if __name__ == "__main__":
    main()
