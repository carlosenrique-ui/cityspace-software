# tests/test_grid_to_pin_height.py

import pytest
from offline.geo.grid_to_pin_height import grid_to_pin_height


def test_pin_height_basic():
    grid_norm = {
        (0, 0): 0.0,
        (0, 1): 0.5,
        (1, 0): 1.0,
    }

    heights = grid_to_pin_height(grid_norm, min_cm=0.0, max_cm=10.0)

    assert heights[(0, 0)] == 0.0
    assert heights[(0, 1)] == 5.0
    assert heights[(1, 0)] == 10.0


def test_pin_height_custom_range():
    grid_norm = {(0, 0): 0.5}

    heights = grid_to_pin_height(grid_norm, min_cm=2.0, max_cm=6.0)

    assert heights[(0, 0)] == 4.0


def test_invalid_normalized_value():
    grid_norm = {(0, 0): 1.2}

    with pytest.raises(ValueError):
        grid_to_pin_height(grid_norm)


def test_invalid_range():
    grid_norm = {(0, 0): 0.5}

    with pytest.raises(ValueError):
        grid_to_pin_height(grid_norm, min_cm=10.0, max_cm=5.0)
