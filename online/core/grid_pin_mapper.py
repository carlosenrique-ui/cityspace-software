# online/core/grid_pin_mapper.py

class GridPinMapper:
    """
    Responsável por mapear (row, col) lógico
    para pin_id físico da mesa.

    Regra:
    - Origem no canto superior direito
    - Zig-zag por linhas
    """

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.total_pins = rows * cols

    def to_pin_id(self, row: int, col: int) -> int:
        """
        Converte (row, col) em pin_id físico.
        """

        if not (0 <= row < self.rows):
            raise ValueError(f"row inválido: {row}")

        if not (0 <= col < self.cols):
            raise ValueError(f"col inválido: {col}")

        # Zig-zag por linha
        if row % 2 == 0:
            # linha par: direita -> esquerda
            pin_id = row * self.cols + (self.cols - 1 - col)
        else:
            # linha ímpar: esquerda -> direita
            pin_id = row * self.cols + col

        return pin_id

    def to_row_col(self, pin_id: int):
        """
        Converte pin_id físico de volta para (row, col).
        Útil para debug, calibração e engenharia.
        """

        if not (0 <= pin_id < self.total_pins):
            raise ValueError(f"pin_id inválido: {pin_id}")

        row = pin_id // self.cols
        offset = pin_id % self.cols

        if row % 2 == 0:
            col = self.cols - 1 - offset
        else:
            col = offset

        return row, col
