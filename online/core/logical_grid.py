# online/core/logical_grid.py

from dataclasses import dataclass


@dataclass(frozen=True)
class LogicalGrid:
    """
    Grid lógico normalizado do CitySpace.

    Convenções:
    - Origem (0,0) no canto SUPERIOR DIREITO
    - x cresce para a ESQUERDA
    - y cresce para BAIXO
    - u, v ∈ [0, 1]
    """

    rows: int
    cols: int

    # --------------------------------------------------
    # PINO → UV (normalizado)
    # --------------------------------------------------
    def pin_to_uv(self, x: int, y: int) -> tuple[float, float]:
        """
        Converte coordenada discreta do pino (x,y)
        para coordenada normalizada (u,v).
        """
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            raise ValueError("Pino fora do grid")

        # origem no canto superior direito
        u = 1.0 - (x / (self.cols - 1))
        v = y / (self.rows - 1)

        return u, v

    # --------------------------------------------------
    # UV → PINO
    # --------------------------------------------------
    def uv_to_pin(self, u: float, v: float) -> tuple[int, int]:
        """
        Converte coordenada normalizada (u,v)
        para pino discreto mais próximo (x,y).
        """
        if not (0.0 <= u <= 1.0 and 0.0 <= v <= 1.0):
            raise ValueError("UV fora do intervalo [0,1]")

        x = round((1.0 - u) * (self.cols - 1))
        y = round(v * (self.rows - 1))

        return x, y
