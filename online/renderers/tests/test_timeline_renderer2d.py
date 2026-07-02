# online/renderers/test_timeline_renderer2d.py

from online.time.construction_timeline import ConstructionTimeline
from online.renderers.renderer2d import Renderer2D
from online.renderers.layer2d import Layer2D
from online.renderers.colormaps import height_colormap


def main():
    rows, cols = 8, 16

    timeline = ConstructionTimeline(
        rows=rows,
        cols=cols,
        max_height=30.0,
        loop=False,
    )

    renderer = Renderer2D(grid_shape=(rows, cols))

    terrain_layer = Layer2D(
        name="terrain",
        grid=timeline.snapshot()["grid"],
        colormap=height_colormap(),
        alpha=1.0,
    )

    renderer.add_layer(terrain_layer)

    # -------------------------------------------------
    # Simula avanço temporal
    # -------------------------------------------------
    for _ in range(20):
        state = timeline.advance()
        terrain_layer.update(state["grid"])

    renderer.render(
        title="Timeline Renderer2D",
        subtitle=f"Frame {state['frame']} | Dir: {state['direction']}",
    )

    print("✔ Timeline Renderer2D OK")


if __name__ == "__main__":
    main()
