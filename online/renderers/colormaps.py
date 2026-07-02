# online/renderers/colormaps.py

from matplotlib.colors import LinearSegmentedColormap


def height_colormap():
    """
    Colormap contínuo para alturas.
    Baixo → Azul
    Médio → Verde / Amarelo
    Alto → Vermelho
    """
    colors = [
        (0.0, "#08306b"),  # azul escuro
        (0.3, "#41ab5d"),  # verde
        (0.6, "#fec44f"),  # amarelo
        (1.0, "#d7301f"),  # vermelho
    ]

    return LinearSegmentedColormap.from_list(
        "height_colormap",
        [c for _, c in colors],
        N=256,
    )
