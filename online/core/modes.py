# online/core/modes.py

from dataclasses import dataclass
from typing import Literal, Dict

from online.core.grid_profile import GridProfile


ModeName = Literal["BAIRRO", "CIDADE", "CORREDOR"]


@dataclass(frozen=True)
class ModeProfile:
    """
    Perfil de operação da mesa CitySpace.
    Define escala, semântica e limites.
    """

    name: ModeName
    description: str

    # Grid
    rows: int
    cols: int
    cell_size_cm: float

    # Visual
    visual_scale: float
    z_amplification: float

    # Agregação de dados
    aggregation_policy: Literal["mean", "sum", "max"]

    # Restrições
    allow_zoom: bool
    allow_pan: bool

    def build_grid_profile(self, bbox_geo):
        """
        Cria o GridProfile correspondente a este modo.
        """
        return GridProfile(
            rows=self.rows,
            cols=self.cols,
            cell_size_cm=self.cell_size_cm,
            bbox_geo=bbox_geo
        )


# ======================================================
# MODOS DEFINIDOS (PONTO ÚNICO DE VERDADE)
# ======================================================

MODES: Dict[ModeName, ModeProfile] = {

    "BAIRRO": ModeProfile(
        name="BAIRRO",
        description="Alta resolução local (análise urbana fina)",
        rows=8,
        cols=16,
        cell_size_cm=1.0,
        visual_scale=1.0,
        z_amplification=1.0,
        aggregation_policy="mean",
        allow_zoom=False,
        allow_pan=False,
    ),

    "CIDADE": ModeProfile(
        name="CIDADE",
        description="Escala urbana agregada (planejamento estratégico)",
        rows=8,
        cols=16,
        cell_size_cm=2.0,   # cada célula representa área maior
        visual_scale=0.6,
        z_amplification=0.7,
        aggregation_policy="mean",
        allow_zoom=True,
        allow_pan=True,
    ),

    "CORREDOR": ModeProfile(
        name="CORREDOR",
        description="Sistema linear (transporte / infraestrutura)",
        rows=4,
        cols=32,
        cell_size_cm=1.5,
        visual_scale=0.8,
        z_amplification=1.2,
        aggregation_policy="sum",
        allow_zoom=False,
        allow_pan=True,
    ),
}
