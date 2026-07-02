# ======================================================
# MOTOR CANÔNICO — GIF TEMPORAL
# Planta Baixa IPT
# ======================================================
#
# RESPONSABILIDADES:
# - Gerar grids temporais em metros reais
# - Renderizar PNGs via Renderer2D
# - Aplicar DXF como overlay fixo
# - Gerar GIF final
#
# ESTE ARQUIVO DEVE SER ESTÁVEL
# ======================================================

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import imageio.v2 as imageio

from online.renderers.renderer2d import Renderer2D
from online.renderers.colormaps import height_colormap


# ------------------------------------------------------
# MODELO TEMPORAL (PODE EVOLUIR DEPOIS)
# ------------------------------------------------------
def generate_grid_at_time(t, n_frames, shape, max_height_m):

    grid = np.zeros(shape)
    progress = t / (n_frames - 1)

    # Exemplos de volumes crescendo
    grid[2:5, 4:7] = max_height_m * progress
    grid[5:7, 10:13] = max_height_m * (progress ** 1.4)

    return grid


# ------------------------------------------------------
# FUNÇÃO PRINCIPAL (CHAMADA PELO TESTE)
# ------------------------------------------------------
def generate_gif(
    n_frames=30,
    max_height_m=30.0,
    gif_fps=6,
    dxf_alpha=0.3
):

    # Configuração da mesa
    rows, cols = 8, 16
    shape = (rows, cols)

    # Saída
    output_dir = "visualization/gif"
    frames_dir = os.path.join(output_dir, "frames")
    gif_path = os.path.join(output_dir, "planta_baixa_ipt_temporal.gif")

    # DXF
    dxf_path = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"

    os.makedirs(frames_dir, exist_ok=True)

    # Renderer (visual apenas)
    renderer = Renderer2D(
        actuator=None,
        grid_shape=shape
    )

    # Carregar DXF uma vez
    gdf = gpd.read_file(dxf_path, layer="entities")
    gdf = gdf[gdf.geom_type == "LineString"]

    frame_paths = []

    # Loop temporal
    for t in range(n_frames):

        grid_m = generate_grid_at_time(
            t, n_frames, shape, max_height_m
        )

        png_path = os.path.join(
            frames_dir,
            f"frame_{t:03d}.png"
        )

        # Render base
        renderer.render_png(
            grid_m=grid_m,
            title="Planta Baixa IPT",
            phase=f"t = {t}",
            save_path=png_path,
            vmin=0,
            vmax=max_height_m,
            colormap=height_colormap(),
        )

        # Overlay DXF
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(plt.imread(png_path))
        ax.axis("off")

        gdf.plot(
            ax=ax,
            color="white",
            linewidth=0.7,
            alpha=dxf_alpha,
            zorder=10
        )

        ax.set_title(
            "Planta Baixa IPT — Evolução Temporal\n"
            "Eixo X: Sentido Bairro | Eixo Y: Sentido Campus"
        )

        plt.tight_layout()
        plt.savefig(png_path, dpi=150)
        plt.close()

        frame_paths.append(png_path)

    # Criar GIF
    images = [imageio.imread(p) for p in frame_paths]
    imageio.mimsave(gif_path, images, fps=gif_fps)

    return gif_path
