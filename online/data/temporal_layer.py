import geopandas as gpd

class TemporalLayer:
    def __init__(self, path, layer):
        self.gdf = gpd.read_file(path, layer=layer)

    def at_time(self, t):
        return self.gdf[
            (self.gdf["t_start"] <= t) &
            (self.gdf["t_end"] >= t)
        ]
