# online/renderers/renderer2d.py

import os
import numpy as np
import matplotlib.pyplot as plt

from online.contracts.construction_frame import ConstructionFrame
from online.contracts.actuator_commands import (
    ActuatorCommand,
    ActuatorCommandType
)


class Renderer2D:
    """
    Renderer 2D canônico da MESA VIRTUAL / FÍSICA.

    Responsabilidades:
    - Renderizar estados espaciais (X, Y, Z)
    - Z SEMPRE em metros (z_real_m)
    - NÃO conhece timeline
    - NÃO conhece player
    - Compatível com atuador virtual e físico

    Este renderer é a base comum entre:
    - Mesa virtual (visualização)
    - Mesa física (pinos eletromecânicos)
    """

    def __init__(self, actuator, grid_shape=(8, 16)):
        """
        :param actuator: Atuador (virtual ou físico). Pode ser None para render visual.
        :param grid_shape: Dimensão da mesa (linhas, colunas)
        """
        self.actuator = actuator
        self.rows, self.cols = grid_shape

    # -------------------------------------------------
    # Render semântico (eventos → atuador)
    # -------------------------------------------------
    def render(self, frame: ConstructionFrame):
        """
        Renderiza um ConstructionFrame emitindo comandos
        para o atuador (virtual ou físico).
        """

        if self.actuator is None:
            return

        for entity in frame.removed:
            self.actuator.execute(
                ActuatorCommand(
                    type=ActuatorCommandType.ERASE,
                    payload=entity
                )
            )

        for entity in frame.updated:
            self.actuator.execute(
                ActuatorCommand(
                    type=ActuatorCommandType.UPDATE,
                    payload=entity
                )
            )

        for entity in frame.created:
            self.actuator.execute(
                ActuatorCommand(
                    type=ActuatorCommandType.DRAW,
                    payload=entity
                )
            )

    # -------------------------------------------------
    # Render VISUAL (PNG) — mesa virtual
    # -------------------------------------------------
    def render_png(
        self,
        grid_m: np.ndarray,
        title: str,
        phase: str,
        save_path: str,
        vmin: float,
        vmax: float,
        colormap
    ):
        """
        Renderiza um grid 2D (em metros) como PNG canônico.

        :param grid_m: matriz 2D com alturas em metros
        :param title: título principal
        :param phase: fase temporal (SCAN, BUILD, etc.)
        :param save_path: caminho do PNG
        :param vmin: altura mínima (normalização)
        :param vmax: altura máxima (normalização)
        :param colormap: colormap contínuo
        """

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        plt.figure(figsize=(8, 4))

        plt.imshow(
            grid_m,
            cmap=colormap,
            origin="upper",  # (0,0) no canto superior esquerdo
            vmin=vmin,
            vmax=vmax,
            interpolation="nearest",
        )

        plt.colorbar(label="Altura (m)")
        plt.xlabel("X (pinos)")
        plt.ylabel("Y (pinos)")

        plt.title(f"{title}\nFase: {phase}")

        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
