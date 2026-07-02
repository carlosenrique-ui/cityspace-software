# offline/geo/test_geojson_to_grid.py

from offline.geo.geojson_to_grid import geojson_to_grid
from online.core.grid_profile import GridProfile


def make_dummy_geojson():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"value": 10},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-46.70, -23.60],
                        [-46.68, -23.60],
                        [-46.68, -23.58],
                        [-46.70, -23.58],
                        [-46.70, -23.60],
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {"value": 20},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-46.68, -23.58],
                        [-46.65, -23.58],
                        [-46.65, -23.55],
                        [-46.68, -23.55],
                        [-46.68, -23.58],
                    ]]
                }
            }
        ]
    }


def test_geojson_to_grid():
    profile = GridProfile(
        rows=8,
        cols=16,
        cell_size_cm=1.0,
        bbox_geo=(-46.70, -23.60, -46.65, -23.55),
    )

    geojson = make_dummy_geojson()

    grid = geojson_to_grid(
        geojson=geojson,
        grid_profile=profile,
        value_property="value",
        aggregation_policy="mean",
    )

    non_zero = {k: v for k, v in grid.items() if v > 0}
    print("Células com dados:", non_zero)

    assert len(non_zero) > 0
    print("✔ GeoJSON → Grid OK")


if __name__ == "__main__":
    test_geojson_to_grid()
