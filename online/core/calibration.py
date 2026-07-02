# online/core/calibration.py

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class GridCalibration:
    """
    Calibração lógica global do grid
    (independente de hardware).
    """
    z_min_cm: float = 0.0
    z_max_cm: float = 10.0
    scale: float = 1.0
    offset_cm: float = 0.0


@dataclass
class PinCalibration:
    """
    Calibração lógica individual de pino.
    """
    offset_cm: float = 0.0
    scale: float = 1.0
    disabled: bool = False


class CalibrationEngine:
    """
    Aplica calibração lógica sobre valores de altura.
    """

    def __init__(
        self,
        grid_calibration: GridCalibration,
        pin_calibrations: Dict[int, PinCalibration] | None = None,
    ):
        self.grid = grid_calibration
        self.pins = pin_calibrations or {}

    def calibrate(
        self,
        pin_id: int,
        z_input_cm: float,
    ) -> float:
        """
        Retorna altura calibrada (cm),
        respeitando limites e offsets.
        """

        # Calibração global
        z = z_input_cm * self.grid.scale + self.grid.offset_cm

        # Calibração individual
        pin = self.pins.get(pin_id)
        if pin:
            if pin.disabled:
                return 0.0
            z = z * pin.scale + pin.offset_cm

        # Saturação
        z = max(self.grid.z_min_cm, z)
        z = min(self.grid.z_max_cm, z)

        return z
