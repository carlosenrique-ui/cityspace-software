from dataclasses import dataclass

@dataclass(frozen=True)
class TemporalState:
    """
    Representa um estado temporal discreto do sistema.
    Equivalente a um 'frame' no tempo.
    """
    index: int
    phase: str
    x: int
    y: int
    z_real_m: float
    z_pin_cm: float
