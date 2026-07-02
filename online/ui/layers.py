# online/ui/layers.py

def make_dummy_urban_geojson():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Rua Principal", "layer": "ruas"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [20, 0], [40, 10]]
                }
            },
            {
                "type": "Feature",
                "properties": {"name": "Edifício A", "layer": "edificios"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [10, 5], [15, 5], [15, 10], [10, 10], [10, 5]
                    ]]
                }
            }
        ]
    }
