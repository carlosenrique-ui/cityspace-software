# online/renderers/test_renderer2d_multilayer.py

import numpy as np

from online.renderers.renderer2d import Renderer2D
from online.renderers.layer2d import Layer2D
from online.renderers.colormaps import height_colormap


def main():
    rows, cols = 8, 16
    shape = (rows, cols)

    renderer = Renderer2D(grid_shape=shape)

    # -------------------------------------------------
    # Layer 1: Terreno (baixo relevo)
    # -------------------------------------------------
    terrain = np.linspace(0, 5, rows * cols).reshape(shape)

    layer_terrain = Layer2D(
        grid=terrain,
        name="Terreno",
        colormap=height_colormap(),
        alpha=1.0,
        vmin=0,
        vmax=30,
        zorder=0,
    )

    # -------------------------------------------------
    # Layer 2: Edifícios (sobrepostos)
    # -------------------------------------------------
    buildings = np.zeros(shape)
    buildings[2:5, 4:7] = 15
    buildings[5:7, 10:13] = 25

    layer_buildings = Layer2D(
        grid=buildings,
        name="Edifícios",
        colormap=height_colormap(),
        alpha=0.7,
        vmin=0,
        vmax=30,
        zorder=1,
    )

    renderer.add_layer(layer_terrain)
    renderer.add_layer(layer_buildings)

    renderer.render(
        title="Renderer2D Multilayer",
        subtitle="Terreno + Edifícios | Simulação Virtual",
        save_path="visualization/debug/renderer2d_multilayer.png",
    )

    print("✔ Renderer2D multilayer OK")


if __name__ == "__main__":
    main()
