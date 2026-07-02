from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class ImageryProvider(ABC):
    """
    Base class for imagery providers.

    An imagery provider is responsible for producing background imagery
    or projected-map references for the Spatial Project.

    Examples:
    - GeoSanja orthophoto
    - OSM tiles
    - Cesium imagery
    - WMTS imagery
    - municipal orthophoto
    """

    provider_name: str = "base_imagery_provider"
    provider_type: str = "imagery"

    def __init__(self, spatial_project_path: str | Path):
        self.spatial_project_path = Path(spatial_project_path)

    @abstractmethod
    def generate_imagery_layer(self) -> Dict[str, Any]:
        raise NotImplementedError
