from __future__ import annotations


class ProviderRegistry:
    """
    Registry for provider discovery.

    This is only the skeleton. Real providers will be registered later.

    Target examples:
    - geosanja_contour_terrain
    - copernicus_dem_terrain
    - microsoft_building_footprints
    - osm_buildings
    - geosanja_orthophoto
    """

    def __init__(self):
        self.terrain_providers = {}
        self.building_providers = {}
        self.imagery_providers = {}

    def register_terrain(self, name, provider_class):
        self.terrain_providers[name] = provider_class

    def register_building(self, name, provider_class):
        self.building_providers[name] = provider_class

    def register_imagery(self, name, provider_class):
        self.imagery_providers[name] = provider_class

    def list_providers(self):
        return {
            "terrain": sorted(self.terrain_providers.keys()),
            "building": sorted(self.building_providers.keys()),
            "imagery": sorted(self.imagery_providers.keys()),
        }
