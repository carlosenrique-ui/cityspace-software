from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from .base_provider import HeightProvider


class SyntheticHeightProvider(HeightProvider):
    """
    Synthetic provider for technical validation.

    It does not use real terrain or buildings.
    It generates a controlled height gradient so that:
    - Height Contract can be tested
    - BMP/CSV can be tested later
    - Physical Table can be validated by technicians
    """

    provider_name = "Synthetic Height Provider"
    provider_type = "synthetic_validation"

    def generate_height_contract(self) -> Dict[str, Any]:
        spatial_project = json.loads(
            self.spatial_project_path.read_text(encoding="utf-8")
        )

        rows = spatial_project["grid"]["rows"]
        cols = spatial_project["grid"]["cols"]

        cells = []

        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                pin_id = (col - 1) * rows + row

                terrain_height_m = 700.0 + row * 0.5
                building_height_m = col * 1.0

                total_height_m = terrain_height_m + building_height_m

                cells.append({
                    "cell_id": f"P{pin_id:03d}",
                    "pin_id": pin_id,
                    "row": row,
                    "col": col,
                    "terrain_height_m": round(terrain_height_m, 4),
                    "building_height_m": round(building_height_m, 4),
                    "total_height_m": round(total_height_m, 4),
                    "relative_height_m": None,
                    "pin_height_cm": None,
                    "gray_value": None,
                    "height_source": self.provider_type,
                })

        cells = self.normalize_to_pin_heights(cells)

        return {
            "contract_type": "height_contract",
            "contract_version": "G5.5",
            "provider": {
                "name": self.provider_name,
                "type": self.provider_type,
            },
            "spatial_project": spatial_project,
            "height_model": {
                "formula": "total_height_m = terrain_height_m + building_height_m",
                "normalization": "relative to minimum total_height_m inside the grid",
                "pin_height_cm_range": [0, 10],
                "gray_value_range": [0, 255],
            },
            "cells": cells,
        }
