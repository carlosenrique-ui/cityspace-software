# online/core/test_logical_grid.py

from online.core.logical_grid import LogicalGrid


def test_logical_grid():
    grid = LogicalGrid(rows=8, cols=16)

    # canto superior direito
    u, v = grid.pin_to_uv(0, 0)
    assert (u, v) == (1.0, 0.0)

    # canto inferior esquerdo
    u, v = grid.pin_to_uv(15, 7)
    assert (round(u, 2), round(v, 2)) == (0.0, 1.0)

    # ida e volta
    x, y = grid.uv_to_pin(u, v)
    assert (x, y) == (15, 7)

    print("✔ LogicalGrid OK")


if __name__ == "__main__":
    test_logical_grid()
