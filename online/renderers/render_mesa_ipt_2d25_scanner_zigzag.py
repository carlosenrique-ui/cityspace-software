# ======================================================
# MESA VIRTUAL IPT — 2D / 2.5D CANÔNICA
# Scanner físico + zig-zag (igual ao PRIMEIRO GIF)
# IPT COMPLETO + ROTAÇÃO EXPLÍCITA
# ======================================================

import os
import time
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from shapely.affinity import rotate
from matplotlib.patches import Rectangle

# ------------------------------------------------------
# CONFIGURAÇÃO DA MESA
# ------------------------------------------------------
ROWS = 8
COLS = 16
N_CELLS = ROWS * COLS
EXTENT = [0, COLS, ROWS, 0]

# ------------------------------------------------------
# ARQUIVOS
# ------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"

OUTPUT_DIR = "visualization/gif"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames_ipt_scanner_zigzag")
GIF_PATH = os.path.join(OUTPUT_DIR, "mesa_ipt_2d25_scanner_zigzag.gif")

# ------------------------------------------------------
# PARÂMETROS VISUAIS
# ------------------------------------------------------
MAX_HEIGHT_M = 30.0
DXF_COLOR = "white"
DXF_ALPHA = 0.85
DXF_LINEWIDTH = 0.9
PIN_COLORMAP = "viridis"
GIF_FPS = 6

# ------------------------------------------------------
# ROTAÇÃO DO IPT (LEGADO)
# ------------------------------------------------------
# ⚠️ AJUSTE SEU VALOR REAL AQUI
IPT_ROTATION_DEG = -28.0  # exemplo: alinhamento com Av. Escola Politécnica

# ------------------------------------------------------
# TEMPO POR CÉLULA
# ------------------------------------------------------
BASE_TIME = 0.04
VAR_TIME = 0.10


def cell_time(row, col):
    cx, cy = COLS / 2, ROWS / 2
    d = np.sqrt((col - cx) ** 2 + (row - cy) ** 2)
    return BASE_TIME + VAR_TIME * d / np.sqrt(cx ** 2 + cy ** 2)


# ------------------------------------------------------
# SCANNER ZIG-ZAG (PRIMEIRO GIF)
# ------------------------------------------------------
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


# ------------------------------------------------------
# NORMALIZAÇÃO + ROTAÇÃO DO DXF
# ------------------------------------------------------
def prepare_dxf(gdf, rows, cols):
    # manter LineString e MultiLineString
    gdf = gdf[gdf.geom_type.isin(["LineString", "MultiLineString"])].copy()

    # rotação explícita (em torno do centro)
    gdf["geometry"] = gdf["geometry"].apply(
        lambda g: rotate(g, IPT_ROTATION_DEG, origin="center", use_radians=False)
    )

    # normalização para o grid
    minx, miny, maxx, maxy = gdf.total_bounds

    def normalize(geom):
        x, y = geom.xy
        x = (np.array(x) - minx) / (maxx - minx) * cols
        y = (np.array(y) - miny) / (maxy - miny) * rows
        return type(geom)(zip(x, y))

    gdf["geometry"] = gdf["geometry"].apply(normalize)
    return gdf


# ------------------------------------------------------
# RENDER FRAME
# ------------------------------------------------------
def render_frame(grid, gdf_dxf, active, idx, path):
    fig, ax = plt.subplots(figsize=(10, 5))

    im = ax.imshow(
        grid, cmap=PIN_COLORMAP, extent=EXTENT,
        origin="upper", vmin=0, vmax=MAX_HEIGHT_M,
        interpolation="nearest", zorder=5
    )

    # IPT SEMPRE POR CIMA
    gdf_dxf.plot(
        ax=ax, color=DXF_COLOR,
        linewidth=DXF_LINEWIDTH,
        alpha=DXF_ALPHA, zorder=8
    )

    r, c = active
    ax.add_patch(Rectangle((c, r), 1, 1,
                           fill=False, edgecolor="white",
                           linewidth=3, zorder=12))

    ax.set_xlabel("Eixo X — Sentido Bairro (Av. Escola Politécnica)")
    ax.set_ylabel("Eixo Y — Sentido Campus (USP)")

    ax.set_title(
        f"Scanner IPT (Zig-Zag)\n"
        f"Célula {idx+1}/{N_CELLS} | (x={c}, y={r})"
    )

    ax.set_xticks(np.arange(0, COLS + 1))
    ax.set_yticks(np.arange(0, ROWS + 1))
    ax.grid(alpha=0.15)
    ax.set_xlim(0, COLS)
    ax.set_ylim(ROWS, 0)

    plt.colorbar(im, ax=ax, label="Altura (m)")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


# ------------------------------------------------------
# PIPELINE
# ------------------------------------------------------
def main():
    os.makedirs(FRAMES_DIR, exist_ok=True)

    gdf = gpd.read_file(DXF_PATH, layer="entities")
    gdf = prepare_dxf(gdf, ROWS, COLS)

    grid = np.zeros((ROWS, COLS))
    frames = []
    path = zigzag_path(ROWS, COLS)

    for i, (r, c) in enumerate(path):
        grid[r, c] = MAX_HEIGHT_M * ((i + 1) / N_CELLS) ** 1.15
        fp = os.path.join(FRAMES_DIR, f"frame_{i:03d}.png")
        render_frame(grid, gdf, (r, c), i, fp)
        frames.append(fp)
        time.sleep(cell_time(r, c))

    imgs = [imageio.imread(f) for f in frames]
    imageio.mimsave(GIF_PATH, imgs, fps=GIF_FPS)

    print("GIF gerado:", GIF_PATH)


if __name__ == "__main__":
    main()
