# ======================================================
# TESTE CANÔNICO — RENDERER2D MULTILAYER (1 LAYER)
# Planta Baixa IPT
# ======================================================
#
# - Uma única layer
# - Nome: Planta Baixa IPT
# - Renderer2D visual (actuator=None)
# - DXF como overlay de referência
#
# ======================================================

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from online.renderers.renderer2d import Renderer2D
from online.renderers.layer2d import Layer2D
from online.renderers.colormaps import height_colormap


def main():

    print("=" * 70)
    print("TESTE: Renderer2D Multilayer — Planta Baixa IPT")
    print("=" * 70)

    # -------------------------------------------------
    # Configuração da mesa virtual
    # -------------------------------------------------
    rows, cols = 8, 16
    shape = (rows, cols)

    # Renderer VISUAL (atuador = None)
    renderer = Renderer2D(None, grid_shape=shape)

    # -------------------------------------------------
    # Grid vazio (layer puramente visual)
    # -------------------------------------------------
    grid_vazio = np.zeros(shape)

    # -------------------------------------------------
    # Layer única: Planta Baixa IPT
    # -------------------------------------------------
    layer_planta = Layer2D(
        grid=grid_vazio,
        name="Planta Baixa IPT",
        colormap=height_colormap(),
        alpha=1.0,
        zorder=0,
    )

    renderer.add_layer(layer_planta)

    # -------------------------------------------------
    # Render base (PNG)
    # -------------------------------------------------
    save_path = "visualization/debug/planta_baixa_ipt_base.png"

    renderer.render(
        title="Planta Baixa IPT",
        subtitle="DXF como referência visual (1 layer)",
        save_path=save_path,
    )

    print("[OK] Render base gerado:", save_path)

    # -------------------------------------------------
    # Overlay DXF (Planta Baixa IPT)
    # -------------------------------------------------
    print("[INFO] Aplicando overlay DXF")

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
    print("Layer única validada: Planta Baixa IPT")
    print("=" * 70)


if __name__ == "__main__":
    main()
