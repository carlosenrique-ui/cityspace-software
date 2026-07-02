from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BuildingProvider(ABC):
    """
    Base class for building providers.

    A building provider is responsible for producing building_height_m
    and/or building footprint information for each grid cell.

    Examples:
    - Municipal footprint provider
    - Microsoft Building Footprints provider
    - Overture Maps provider
    - OpenStreetMap provider
    - Drone DSM/DTM derived building provider
    """

    provider_name: str = "base_building_provider"
    provider_type: str = "building"

    def __init__(self, spatial_project_path: str | Path):
        self.spatial_project_path = Path(spatial_project_path)

    @abstractmethod
    def generate_building_layer(self) -> Dict[str, Any]:
        raise NotImplementedError
