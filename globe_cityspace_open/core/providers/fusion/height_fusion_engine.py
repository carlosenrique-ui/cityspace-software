from __future__ import annotations

from typing import Any, Dict, List


class HeightFusionEngine:
    """
    Combines terrain and building layers into a Height Contract.

    terrain_height_m + building_height_m = total_height_m

    This engine must remain provider-independent.
    """

    def __init__(
        self,
        terrain_layer: Dict[str, Any],
        building_layer: Dict[str, Any],
        max_pin_height_cm: float = 10.0,
    ):
        self.terrain_layer = terrain_layer
        self.building_layer = building_layer
        self.max_pin_height_cm = max_pin_height_cm

    def generate_height_contract(self) -> Dict[str, Any]:
        terrain_cells = {
            c["cell_id"]: c
            for c in self.terrain_layer["cells"]
        }

        building_cells = {
            c["cell_id"]: c
            for c in self.building_layer["cells"]
        }

        cells: List[Dict[str, Any]] = []

        for cell_id, terrain_cell in terrain_cells.items():
            building_cell = building_cells.get(cell_id, {})

            terrain_height_m = float(
                terrain_cell.get("terrain_height_m", 0.0)
            )

            building_height_m = float(
                building_cell.get("building_height_m", 0.0)
            )

            total_height_m = terrain_height_m + building_height_m

            cells.append({
                "cell_id": cell_id,
                "pin_id": terrain_cell.get("pin_id"),
                "row": terrain_cell.get("row"),
                "col": terrain_cell.get("col"),
                "terrain_height_m": round(terrain_height_m, 4),
                "building_height_m": round(building_height_m, 4),
                "total_height_m": round(total_height_m, 4),
                "relative_height_m": None,
                "pin_height_cm": None,
                "gray_value": None,
                "terrain_source": self.terrain_layer.get("provider"),
                "building_source": self.building_layer.get("provider"),
            })

        return self._normalize(cells)

    def _normalize(self, cells: List[Dict[str, Any]]) -> Dict[str, Any]:
        values = [
            c["total_height_m"]
            for c in cells
        ]

        z_min = min(values)
        z_max = max(values)
        dz = z_max - z_min

        for c in cells:
            relative = c["total_height_m"] - z_min

            if dz == 0:
                pin_height_cm = 0.0
            else:
                pin_height_cm = (
                    relative / dz
                ) * self.max_pin_height_cm

            gray_value = round(
                (pin_height_cm / self.max_pin_height_cm) * 255
            )

            c["relative_height_m"] = round(relative, 4)
            c["pin_height_cm"] = round(pin_height_cm, 4)
            c["gray_value"] = int(gray_value)

        return {
            "contract_type": "height_contract",
            "contract_version": "G5.9",
            "fusion_engine": "HeightFusionEngine",
            "height_model": {
                "formula": "total_height_m = terrain_height_m + building_height_m",
                "normalization": "relative to minimum total_height_m inside the grid",
                "pin_height_cm_range": [0, self.max_pin_height_cm],
                "gray_value_range": [0, 255],
            },
            "cells": cells,
        }
