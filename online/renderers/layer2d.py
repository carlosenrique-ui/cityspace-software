# online/renderers/layer2d.py

import numpy as np


class Layer2D:
    """
    Representa uma camada 2D renderizável.
    Compatível com Renderer2D (multilayer + timeline).
    """

    def __init__(
        self,
        name: str,
        grid: np.ndarray,
        colormap,
        alpha: float = 1.0,
        visible: bool = True,
        zorder: int = 0,
    ):
        self.name = name
        self.grid = np.array(grid, dtype=float)
        self.colormap = colormap
        self.alpha = alpha
        self.visible = visible
        self.zorder = zorder

    # -------------------------------------------------
    # Contrato com Renderer2D
    # -------------------------------------------------
    def validate(self):
        if not isinstance(self.grid, np.ndarray):
            raise TypeError("Layer2D.grid deve ser numpy.ndarray")

        if self.grid.ndim != 2:
            raise ValueError("Layer2D.grid deve ser 2D")

        if self.colormap is None:
            raise ValueError("Layer2D.colormap não pode ser None")

        if not isinstance(self.zorder, int):
            raise TypeError("Layer2D.zorder deve ser int")

    # -------------------------------------------------
    # Atualização temporal
    # -------------------------------------------------
    def update(self, grid: np.ndarray):
        self.grid = np.array(grid, dtype=float)

    # -------------------------------------------------
    # Snapshot (debug / inspeção)
    # -------------------------------------------------
    def snapshot(self):
        return {
            "name": self.name,
            "grid": self.grid.copy(),
            "alpha": self.alpha,
            "visible": self.visible,
            "zorder": self.zorder,
        }
