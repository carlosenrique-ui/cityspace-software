# ======================================================
# MESA VIRTUAL IPT — 2D / 2.5D CANÔNICO
# Integra legado + correções geométricas
# ======================================================
#
# - Grid físico 8x16 (pinos)
# - Planta Baixa IPT (DXF) encaixada
# - Dados em metros reais
# - Leitura humana / projeção
# - Base para mesa real
#
# ======================================================

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import imageio.v2 as imageio

# ------------------------------------------------------
# CONFIGURAÇÃO DA MESA (FÍSICA)
# ------------------------------------------------------
ROWS = 8
COLS = 16
GRID_SHAPE = (ROWS, COLS)

# Extent físico da mesa (coordenadas abstratas de pino)
# (0,0) canto superior esquerdo
EXTENT = [0, COLS, ROWS, 0]

# ------------------------------------------------------
# ARQUIVOS
# ------------------------------------------------------
DXF_PATH = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"

OUTPUT_DIR = "visualization/gif"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames_ipt_2d25")
GIF_PATH = os.path.join(OUTPUT_DIR, "mesa_ipt_2d25_temporal.gif")

# ------------------------------------------------------
# PARÂMETROS VISUAIS (PROJEÇÃO)
# ------------------------------------------------------
N_FRAMES = 45
GIF_FPS = 5

MAX_HEIGHT_M = 30.0

DXF_COLOR = "#DDDDDD"   # cinza claro, não compete
DXF_ALPHA = 0.30

PIN_COLORMAP = "viridis"  # perceptualmente uniforme

# ------------------------------------------------------
# MODELO TEMPORAL (LEGADO REFINADO)
# ------------------------------------------------------
def grid_at_time(t, n_frames):
    """
    Gera um grid 2.5D em metros.
    Crescimento perceptivo (não linear).
    """
    grid = np.zeros(GRID_SHAPE)

    progress = (t / (n_frames - 1)) ** 1.25

    # volumes exemplares (placeholder semântico)
    grid[2:5, 4:7] = MAX_HEIGHT_M * progress
    grid[4:7, 9:13] = MAX_HEIGHT_M * (progress ** 1.1)

    return grid


# ------------------------------------------------------
# RENDER FRAME ÚNICO
# ------------------------------------------------------
def render_frame(grid_m, gdf_dxf, t, save_path):

    fig, ax = plt.subplots(figsize=(10, 5))

    # ------------------------------
    # BASE: PLANTA BAIXA IPT (DXF)
    # ------------------------------
    gdf_dxf.plot(
        ax=ax,
        color=DXF_COLOR,
        linewidth=0.8,
        alpha=DXF_ALPHA,
        zorder=1
    )

    # ------------------------------
    # DADOS: PINOS / ALTURA
    # ------------------------------
    im = ax.imshow(
        grid_m,
        cmap=PIN_COLORMAP,
        extent=EXTENT,
        origin="upper",
        vmin=0,
        vmax=MAX_HEIGHT_M,
        interpolation="nearest",
        zorder=5
    )

    # ------------------------------
    # EIXOS SEMÂNTICOS (ORDENS SUAS)
    # ------------------------------
    ax.set_xlabel("Eixo X — Sentido Bairro (Av. Escola Politécnica)")
    ax.set_ylabel("Eixo Y — Sentido Campus (USP)")

    ax.set_title(
        f"Mesa Virtual IPT — Evolução Temporal\n"
        f"Tempo = {t:02d}"
    )

    # Grade leve para leitura de pinos
    ax.set_xticks(np.arange(0, COLS + 1, 1))
    ax.set_yticks(np.arange(0, ROWS + 1, 1))
    ax.grid(color="black", alpha=0.15, linewidth=0.5)

    # Barra de cores (altura real)
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Altura (m)")

    ax.set_xlim(0, COLS)
    ax.set_ylim(ROWS, 0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


# ------------------------------------------------------
# PIPELINE PRINCIPAL
# ------------------------------------------------------
def main():

    print("=" * 70)
    print("MESA VIRTUAL IPT — 2D / 2.5D (LEGADO INTEGRADO)")
    print("=" * 70)

    os.makedirs(FRAMES_DIR, exist_ok=True)

    # ------------------------------
    # CARREGAR DXF (UMA VEZ)
    # ------------------------------
    gdf = gpd.read_file(DXF_PATH, layer="entities")
    gdf = gdf[gdf.geom_type == "LineString"]

    # Normalizar DXF para o grid (LEGADO)
    minx, miny, maxx, maxy = gdf.total_bounds

    def normalize_geom(geom):
        x, y = geom.xy
        x = (np.array(x) - minx) / (maxx - minx) * COLS
        y = (np.array(y) - miny) / (maxy - miny) * ROWS
        return type(geom)(zip(x, y))

    gdf["geometry"] = gdf["geometry"].apply(normalize_geom)

    # ------------------------------
    # GERAR FRAMES
    # ------------------------------
    frame_paths = []

    for t in range(N_FRAMES):
        print(f"[FRAME {t+1}/{N_FRAMES}]")

        grid = grid_at_time(t, N_FRAMES)

        frame_path = os.path.join(
            FRAMES_DIR,
            f"frame_{t:03d}.png"
        )

        render_frame(
            grid_m=grid,
            gdf_dxf=gdf,
            t=t,
            save_path=frame_path
        )

        frame_paths.append(frame_path)

    # ------------------------------
    # GERAR GIF FINAL
    # ------------------------------
    images = [imageio.imread(fp) for fp in frame_paths]
    imageio.mimsave(GIF_PATH, images, fps=GIF_FPS)

    print("=" * 70)
    print("GIF GERADO COM SUCESSO")
    print("Arquivo:", GIF_PATH)
    print("=" * 70)


if __name__ == "__main__":
    main()
