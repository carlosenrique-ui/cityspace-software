# online/core/temporal_sequence.py

from typing import List
import numpy as np

from online.core.temporal_state import TemporalState


class TemporalSequenceBuilder:
    """
    Constrói uma sequência temporal discreta a partir de um grid.
    """

    def __init__(self, grid_rows: int, grid_cols: int):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

    def build(self, grid_m: np.ndarray, phases: List[dict]) -> List[TemporalState]:
        sequence: List[TemporalState] = []
        index = 0

        for phase in phases:
            phase_name = phase.get("name", "UNKNOWN")

            for y in range(self.grid_rows):
                for x in range(self.grid_cols):
                    z_real_m = float(grid_m[y, x])
                    z_pin_cm = min(z_real_m * 100.0, 10.0)

                    state = TemporalState(
                        index=index,
                        phase=phase_name,
                        x=x,
                        y=y,
                        z_real_m=z_real_m,
                        z_pin_cm=z_pin_cm,
                    )

                    sequence.append(state)
                    index += 1

        return sequence
