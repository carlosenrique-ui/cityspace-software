from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class TerrainProvider(ABC):
    """
    Base class for terrain providers.

    A terrain provider is responsible for producing terrain_height_m
    for each grid cell in a Spatial Project.

    Examples:
    - GeoSanja contour provider
    - Copernicus DEM provider
    - SRTM provider
    - Drone DTM provider
    - Municipal IDE provider
    """

    provider_name: str = "base_terrain_provider"
    provider_type: str = "terrain"

    def __init__(self, spatial_project_path: str | Path):
        self.spatial_project_path = Path(spatial_project_path)

    @abstractmethod
    def generate_terrain_layer(self) -> Dict[str, Any]:
        raise NotImplementedError
