# tests/test_geo_cells.py

from shapely.geometry import Polygon
from offline.geo.geojson_to_cells import aggregate_geometries_to_cells


def test_single_polygon_single_cell():
    # célula 1x1
    cells = {
        (0, 0): Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    }

    # polígono que cobre exatamente a célula
    geometries = [
        Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    ]
    values = [10.0]

    grid = aggregate_geometries_to_cells(
        geometries, values, cells, agg="mean"
    )

    assert grid[(0, 0)] == 10.0


def test_polygon_over_two_cells_mean():
    cells = {
        (0, 0): Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        (0, 1): Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
    }

    geometries = [
        Polygon([(0.5, 0), (1.5, 0), (1.5, 1), (0.5, 1)])
    ]
    values = [20.0]

    grid = aggregate_geometries_to_cells(
        geometries, values, cells, agg="mean"
    )

    assert grid[(0, 0)] == 20.0
    assert grid[(0, 1)] == 20.0


def test_multiple_geometries_sum():
    cells = {
        (0, 0): Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    }

    geometries = [
        Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
    ]
    values = [5.0, 7.0]

    grid = aggregate_geometries_to_cells(
        geometries, values, cells, agg="sum"
    )

    assert grid[(0, 0)] == 12.0


def test_empty_cell_returns_zero():
    cells = {
        (0, 0): Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    }

    geometries = []
    values = []

    grid = aggregate_geometries_to_cells(
        geometries, values, cells, agg="mean"
    )

    assert grid[(0, 0)] == 0.0
