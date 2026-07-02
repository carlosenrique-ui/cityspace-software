# tests/test_path.py

from runner.path import zigzag_scan


def test_zigzag_scan_size():
    rows, cols = 8, 16
    path = zigzag_scan(rows, cols)

    assert len(path) == rows * cols


def test_zigzag_scan_unique_cells():
    rows, cols = 8, 16
    path = zigzag_scan(rows, cols)

    assert len(set(path)) == rows * cols


def test_zigzag_scan_bounds():
    rows, cols = 8, 16
    path = zigzag_scan(rows, cols)

    for row, col in path:
        assert 0 <= row < rows
        assert 0 <= col < cols


def test_zigzag_scan_order_first_rows():
    rows, cols = 3, 4
    path = zigzag_scan(rows, cols)

    expected = [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 3), (1, 2), (1, 1), (1, 0),
        (2, 0), (2, 1), (2, 2), (2, 3),
    ]

    assert path == expected
