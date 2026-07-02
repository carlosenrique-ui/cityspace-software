# ======================================================
# TESTE CANÔNICO — PLANTA BAIXA IPT (1 LAYER)
# Renderer2D + DXF overlay
# ======================================================
#
# - Uma única layer (grid)
# - Renderer2D API REAL
# - DXF como overlay visual
# - Base sólida para FASE C.5 (tempo)
#
# ======================================================

import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from online.renderers.renderer2d import Renderer2D
from online.renderers.colormaps import height_colormap


def main():

    print("=" * 70)
    print("TESTE: Planta Baixa IPT — Single Layer")
    print("=" * 70)

    # -------------------------------------------------
    # Configuração da mesa
    # -------------------------------------------------
    rows, cols = 8, 16
    shape = (rows, cols)

    renderer = Renderer2D(
        actuator=None,
        grid_shape=shape
    )

    # -------------------------------------------------
    # Layer única (grid base)
    # -------------------------------------------------
    grid_m = np.zeros(shape)

    # -------------------------------------------------
    # Render PNG base
    # -------------------------------------------------
    save_path = "visualization/debug/planta_baixa_ipt.png"

    renderer.render_png(
        grid_m=grid_m,
        title="Planta Baixa IPT",
        phase="BASE",
        save_path=save_path,
        vmin=0,
        vmax=1,
        colormap=height_colormap(),
    )

    print("[OK] PNG base gerado:", save_path)

    # -------------------------------------------------
    # Aplicar DXF como overlay visual
    # -------------------------------------------------
    print("[INFO] Aplicando DXF como overlay")

    dxf_path = "/mnt/c/IPT-CitySpace-2018/data/vetor/dxf_corrigido.dxf"

    gdf = gpd.read_file(dxf_path, layer="entities")
    gdf = gdf[gdf.geom_type == "LineString"]

    fig, ax = plt.subplots(figsize=(8, 4))

    img = plt.imread(save_path)
    ax.imshow(img)
    ax.axis("off")

    gdf.plot(
        ax=ax,
        color="white",
        linewidth=0.8,
        alpha=0.7,
        zorder=10
    )

    ax.set_title(
        "Planta Baixa IPT\n"
        "Eixo X: Sentido Bairro | Eixo Y: Sentido Campus"
    )

    plt.tight_layout()
    plt.show()

    print("=" * 70)
    print("TESTE FINALIZADO COM SUCESSO")
    print("Planta Baixa IPT validada (single layer)")
    print("=" * 70)


if __name__ == "__main__":
    main()
