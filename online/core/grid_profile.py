# online/core/grid_profile.py

from dataclasses import dataclass
from typing import Tuple

from online.core.logical_grid import LogicalGrid


@dataclass(frozen=True)
class GridProfile:
    """
    Define como o grid lógico se projeta:
    - no mundo físico (mesa)
    - no mundo geográfico (GeoJSON / mapa)
    """

    rows: int
    cols: int

    # dimensão física da célula
    cell_size_cm: float

    # bounding box geográfica (lon/lat)
    # (min_lon, min_lat, max_lon, max_lat)
    bbox_geo: Tuple[float, float, float, float]

    # --------------------------------------------------
    # GRID LÓGICO
    # --------------------------------------------------
    @property
    def logical_grid(self) -> LogicalGrid:
        return LogicalGrid(rows=self.rows, cols=self.cols)

    # --------------------------------------------------
    # PINO → MUNDO FÍSICO (cm)
    # --------------------------------------------------
    def pin_to_physical_cm(self, x: int, y: int) -> Tuple[float, float]:
        """
        Retorna a posição física do centro da célula (em cm),
        com origem no canto superior direito da mesa.
        """
        X_cm = x * self.cell_size_cm
        Y_cm = y * self.cell_size_cm
        return X_cm, Y_cm

    # --------------------------------------------------
    # PINO → GEO (lon, lat)
    # --------------------------------------------------
    def pin_to_geo(self, x: int, y: int) -> Tuple[float, float]:
        """
        Converte um pino (x,y) para coordenadas geográficas (lon, lat),
        usando interpolação linear na bounding box.
        """
        u, v = self.logical_grid.pin_to_uv(x, y)

        min_lon, min_lat, max_lon, max_lat = self.bbox_geo

        lon = min_lon + u * (max_lon - min_lon)
        lat = max_lat - v * (max_lat - min_lat)

        return lon, lat
