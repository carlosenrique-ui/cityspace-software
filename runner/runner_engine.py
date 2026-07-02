"""
Runner Engine
=============

Executa a lógica temporal e espacial da mesa (virtual ou real).

- Percurso: zig-zag
- Tempo: deslocamento + subida/descida de pino
- Atuador: abstrato (virtual agora, físico no futuro)
"""

from typing import List, Tuple, Dict
import time


class RunnerEngine:
    def __init__(
        self,
        grid: List[List[float]],
        path: List[Tuple[int, int]],
        actuator,
        timing: Dict[str, float],
        realtime: bool = False,
    ):
        self.grid = grid
        self.path = path
        self.actuator = actuator
        self.timing = timing
        self.realtime = realtime

        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    # -----------------------------
    # Execução
    # -----------------------------

    def run(self):
        # Reset inicial
        self.actuator.reset()

        for row, col in self.path:
            height = self._get_cell_height(row, col)

            # mover
            self.actuator.move(row=row, col=col)
            self._wait(self.timing.get("move", 0.0))

            # subir pino
            self.actuator.set_height_cm(height)
            self._wait(self.timing.get("pin", 0.0))

            # segurar
            self._wait(self.timing.get("hold", 0.0))

        # Reset final
        self.actuator.reset()

    # -----------------------------
    # Helpers
    # -----------------------------

    def _get_cell_height(self, row: int, col: int) -> float:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            value = self.grid[row][col]
            return float(value) if value is not None else 0.0
        return 0.0

    def _wait(self, seconds: float):
        if self.realtime and seconds > 0:
            time.sleep(seconds)
