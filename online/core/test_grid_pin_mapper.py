# online/core/test_grid_pin_mapper.py

from online.core.grid_pin_mapper import GridPinMapper


def test_grid_pin_mapper():
    mapper = GridPinMapper(rows=8, cols=16)

    # Canto superior direito
    assert mapper.to_pin_id(0, 0) == 15

    # Canto superior esquerdo
    assert mapper.to_pin_id(0, 15) == 0

    # Linha 1 (zig invertido)
    assert mapper.to_pin_id(1, 0) == 16
    assert mapper.to_pin_id(1, 15) == 31

    # Teste inverso
    for row in range(8):
        for col in range(16):
            pid = mapper.to_pin_id(row, col)
            r2, c2 = mapper.to_row_col(pid)
            assert (row, col) == (r2, c2)

    print("✔ GridPinMapper OK")


if __name__ == "__main__":
    test_grid_pin_mapper()
