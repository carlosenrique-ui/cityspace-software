# online/renderers/visual_snapshot_adapter.py

import numpy as np


class VisualSnapshotAdapter:
    """
    Adapter canônico:
    - Converte snapshot do VisualActuator
    - Em grid 2D (numpy)
    - Compatível com Renderer2D
    """

    def __init__(self, rows: int, cols: int, default_value: float = 0.0):
        self.rows = rows
        self.cols = cols
        self.default_value = default_value

    def to_grid(self, snapshot: dict) -> np.ndarray:
        """
        snapshot: dict vindo de VisualActuator.snapshot()
        Retorna: np.ndarray (rows x cols) com z_real_m
        """

        grid = np.full(
            (self.rows, self.cols),
            self.default_value,
            dtype=float
        )

        for pin_id, data in snapshot.items():
            x = data["x"]
            y = data["y"]
            z = data["z_real_m"]

            if x is None or y is None:
                continue

            # 🔑 Convenção DEFINITIVA
            # (0,0) canto superior esquerdo
            # y cresce para baixo
            if 0 <= y < self.rows and 0 <= x < self.cols:
                grid[y, x] = z

        return grid
