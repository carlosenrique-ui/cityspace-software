from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List


class HeightProvider(ABC):
    """
    Base class for all height providers.

    Every provider must receive a spatial_project.json and produce
    the same Height Contract structure.

    The table pipeline must not care whether heights came from:
    - estimated DEM + footprints
    - drone DSM/DTM
    - LiDAR
    - municipal IDE
    - 3D Tiles
    """

    provider_name: str = "base"
    provider_type: str = "abstract"

    def __init__(self, spatial_project_path: str | Path):
        self.spatial_project_path = Path(spatial_project_path)

    @abstractmethod
    def generate_height_contract(self) -> Dict[str, Any]:
        raise NotImplementedError

    def normalize_to_pin_heights(
        self,
        cells: List[Dict[str, Any]],
        max_pin_height_cm: float = 10.0,
    ) -> List[Dict[str, Any]]:
        total_values = [
            c["total_height_m"]
            for c in cells
        ]

        z_min = min(total_values)
        z_max = max(total_values)
        dz = z_max - z_min

        for c in cells:
            relative = c["total_height_m"] - z_min

            if dz == 0:
                pin_cm = 0.0
            else:
                pin_cm = (relative / dz) * max_pin_height_cm

            gray = round((pin_cm / max_pin_height_cm) * 255)

            c["relative_height_m"] = round(relative, 4)
            c["pin_height_cm"] = round(pin_cm, 4)
            c["gray_value"] = int(gray)

        return cells
