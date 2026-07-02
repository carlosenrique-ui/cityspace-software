from __future__ import annotations

import json
from pathlib import Path


class CitySpaceCoreAdapter:
    """
    Adapter boundary between Globe-CitySpace and IPT-CitySpace.

    Rule:
    - Globe-CitySpace does not call old online/offline modules directly.
    - Globe-CitySpace writes contracts.
    - IPT-CitySpace consumes contracts.
    """

    def __init__(self, spatial_project_path: str | Path):
        self.spatial_project_path = Path(spatial_project_path)
        self.spatial_project = self._load_spatial_project()

    def _load_spatial_project(self) -> dict:
        if not self.spatial_project_path.exists():
            raise FileNotFoundError(
                f"Spatial project not found: {self.spatial_project_path}"
            )

        return json.loads(
            self.spatial_project_path.read_text(encoding="utf-8")
        )

    def validate(self) -> dict:
        required = [
            "contract_type",
            "contract_version",
            "project_name",
            "center",
            "scale",
            "grid",
            "spatial_layout_file",
        ]

        missing = [
            key for key in required
            if key not in self.spatial_project
        ]

        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "contract_type": self.spatial_project.get("contract_type"),
            "contract_version": self.spatial_project.get("contract_version"),
            "project_name": self.spatial_project.get("project_name"),
        }

    def describe_boundary(self) -> dict:
        return {
            "producer": "Globe-CitySpace Explorer",
            "consumer": "IPT-CitySpace Runtime",
            "boundary_contract": str(self.spatial_project_path),
            "direct_legacy_imports_allowed": False,
        }
