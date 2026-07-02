# online/renderers/test_renderer2d.py

"""
Teste simples do Renderer2D em modo VISUAL.
Não envolve timeline.
Não envolve mesa física.
Serve apenas para validar:
- eixos
- colormap
- alturas em metros
"""

import numpy as np

from online.renderers.renderer2d import Renderer2D
from online.renderers.colormaps import height_colormap


def main():
    rows, cols = 8, 16

    # -------------------------------------------------
    # Grid dummy em METROS (z_real_m)
    # (0,0) canto superior esquerdo
    # -------------------------------------------------
    grid_m = np.zeros((rows, cols), dtype=float)

    value = 0.0
    for x in range(cols):
        y_range = range(rows) if x % 2 == 0 else reversed(range(rows))
        for y in y_range:
            grid_m[y, x] = value
            value += 0.2  # 20 cm por passo

    vmin = 0.0
    vmax = grid_m.max()

    renderer = Renderer2D(
        actuator=None,
        grid_shape=(rows, cols)
    )

    renderer.render_png(
        grid_m=grid_m,
        title="Teste Renderer2D",
        phase="TEST",
        save_path="visualization/debug/test_renderer2d.png",
        vmin=vmin,
        vmax=vmax,
        colormap=height_colormap(),
    )

    print("✔ test_renderer2d OK — PNG gerado em visualization/debug")


if __name__ == "__main__":
    main()
