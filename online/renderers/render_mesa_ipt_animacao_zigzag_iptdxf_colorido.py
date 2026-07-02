#!/usr/bin/env python3
# ==========================================================
# MESA VIRTUAL IPT — ANIMAÇÃO ZIG-ZAG
# - IPT visível (normalizado para a mesa)
# - Cores de altura visíveis
# - Tempo perceptível por célula
# ==========================================================

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.affinity import scale, translate
from matplotlib import patches
from matplotlib.animation import FuncAnimation

# ----------------------------------------------------------
# CONFIGURAÇÃO
# ----------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/dxf/IPT-2018-DXF.dxf"

OUT_GIF = "visualization/gif/mesa_ipt_animacao_zigzag_iptdxf_colorido.gif"
os.makedirs(os.path.dirname(OUT_GIF), exist_ok=True)

ROWS, COLS = 8, 16
FPS = 8

T_MIN = 4
T_MAX = 18

SUBDIV = 10
COLORMAP = plt.cm.viridis
ALPHA_GRID = 0.8

# ----------------------------------------------------------
# ALTURAS (SINTÉTICAS — VISUAL)
# ----------------------------------------------------------
np.random.seed(5)
heights = np.random.rand(ROWS, COLS)
h_norm = (heights - heights.min()) / (heights.max() - heights.min())

# ----------------------------------------------------------
# ZIG-ZAG (COLUNA A COLUNA)
# ----------------------------------------------------------
scan_order = []
for c in range(COLS):
    rows = range(ROWS) if c % 2 == 0 else reversed(range(ROWS))
    for r in rows:
        scan_order.append((r, c))

frames = []
for r, c in scan_order:
    t = int(T_MIN + h_norm[r, c] * (T_MAX - T_MIN))
    for k in range(t):
        frames.append((r, c, k / max(t - 1, 1)))

# ----------------------------------------------------------
# CARREGAR E NORMALIZAR DXF PARA A MESA
# ----------------------------------------------------------
gdf = gpd.read_file(DXF_PATH, layer="entities")

minx, miny, maxx, maxy = gdf.total_bounds

sx = COLS / (maxx - minx)
sy = ROWS / (maxy - miny)

gdf["geometry"] = gdf["geometry"].apply(
    lambda g: translate(
        scale(g, xfact=sx, yfact=sy, origin=(minx, maxy)),
        xoff=-minx * sx,
        yoff=-maxy * sy,
    )
)

# ----------------------------------------------------------
# FIGURA
# ----------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_aspect("equal")
ax.set_xlim(0, COLS)
ax.set_ylim(ROWS, 0)
ax.axis("off")
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

# IPT em branco (fundo)
gdf.plot(
    ax=ax,
    color="white",
    linewidth=0.6,
    alpha=0.35,
    zorder=1
)

# Grid colorido (alturas)
grid_img = ax.imshow(
    heights,
    extent=[0, COLS, ROWS, 0],
    cmap=COLORMAP,
    alpha=ALPHA_GRID,
    vmin=0,
    vmax=1,
    zorder=2,
)

# Sub-grid fino
for c in range(COLS):
    for s in range(1, SUBDIV):
        ax.plot(
            [c + s / SUBDIV, c + s / SUBDIV],
            [0, ROWS],
            color="white",
            alpha=0.06,
            linewidth=0.4,
        )

for r in range(ROWS):
    for s in range(1, SUBDIV):
        ax.plot(
            [0, COLS],
            [r + s / SUBDIV, r + s / SUBDIV],
            color="white",
            alpha=0.06,
            linewidth=0.4,
        )

# Célula ativa
active_rect = patches.Rectangle(
    (0, 0),
    1,
    1,
    linewidth=3,
    edgecolor="white",
    facecolor="none",
    zorder=5,
)
fill_rect = patches.Rectangle(
    (0, 0),
    1,
    1,
    linewidth=0,
    facecolor="white",
    alpha=0.0,
    zorder=4,
)

ax.add_patch(fill_rect)
ax.add_patch(active_rect)

# ----------------------------------------------------------
# UPDATE
# ----------------------------------------------------------
def update(i):
    r, c, phase = frames[i]
    active_rect.set_xy((c, r))
    fill_rect.set_xy((c, r))
    fill_rect.set_alpha(0.15 + 0.25 * np.sin(np.pi * phase))
    return active_rect, fill_rect

# ----------------------------------------------------------
# ANIMAÇÃO
# ----------------------------------------------------------
anim = FuncAnimation(
    fig,
    update,
    frames=len(frames),
    interval=1000 / FPS,
    blit=True,
)

print("=" * 60)
print("Gerando GIF com IPT + cores + tempo perceptível")
print(f"Frames totais: {len(frames)}")
print(f"Arquivo: {OUT_GIF}")

anim.save(OUT_GIF, writer="pillow", fps=FPS)

plt.close(fig)

print("GIF gerado com sucesso")
print("=" * 60)
