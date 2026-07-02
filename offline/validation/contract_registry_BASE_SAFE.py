from __future__ import annotations
from pathlib import Path
from typing import Dict, Any

def build_contract(base_dir: Path) -> Dict[str, Any]:
    engine_root = base_dir.resolve()

    return {
        "meta": {
            "system_name": "IPT-CitySpace",
            "version": "3.0-base-safe",
            "contract_mode": "evolutionary",
            "critical_system": True,
        },

        "paths": {
            "scientific_grid_csv": str(
                engine_root / "offline/products/scientific/grid_metrics_utm.csv"
            )
        },

        "reference_systems": [
            "utm",
            "cartesian_trigonometric",
            "physical_table"
        ],

        "grid": {
            "cells_are_square": True,
            "urban_centered": True,
            "outside_value": "NaN",
            "nan_meaning": "no_drone_survey",
            "survey_year": 2018
        },

        "table": {
            "shape": (8, 16),
            "cell_cm": [1, 2],
            "max_z_cm": 10.0,
            "scan": "zigzag",
            "actuation": "centroid"
        },

        "geometry": {
            "rotation_parametric": True,
            "pca_guided": True,
            "rotation_history": [146.815825, 154.0],
            "horizontal_scale": True,
            "vertical_scale": True,
            "north_tilt": True
        },

        "temporal": {
            "x_is_time": True,
            "start": 1940,
            "end": 2020,
            "step": 5
        },

        "dxf": {
            "is_input": True,
            "used_for_validation": True
        }
    }
