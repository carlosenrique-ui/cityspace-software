# tests/test_grid_normalization.py

import pytest
from offline.geo.grid_normalization import normalize_grid


def test_min_max_normalization_basic():
    grid = {
        (0, 0): 10.0,
        (0, 1): 20.0,
        (1, 0): 30.0,
    }

    norm = normalize_grid(grid, method="min_max")

    assert norm[(0, 0)] == 0.0
    assert norm[(1, 0)] == 1.0
    assert norm[(0, 1)] == 0.5


def test_min_max_all_equal():
    grid = {
        (0, 0): 5.0,
        (0, 1): 5.0,
    }

    norm = normalize_grid(grid, method="min_max")

    assert all(v == 0.0 for v in norm.values())


def test_clamp_normalization_basic():
    grid = {
        (0, 0): 0.0,
        (0, 1): 10.0,
        (1, 0): 20.0,
        (1, 1): 30.0,
    }

    norm = normalize_grid(
        grid,
        method="clamp",
        min_value=0.0,
        max_value=20.0,
    )

    assert norm[(0, 0)] == 0.0
    assert norm[(0, 1)] == 0.5
    assert norm[(1, 0)] == 1.0
    assert norm[(1, 1)] == 1.0  # saturado


def test_clamp_requires_bounds():
    grid = {(0, 0): 10.0}

    with pytest.raises(ValueError):
        normalize_grid(grid, method="clamp")


def test_invalid_method():
    grid = {(0, 0): 10.0}

    with pytest.raises(ValueError):
        normalize_grid(grid, method="foo")
