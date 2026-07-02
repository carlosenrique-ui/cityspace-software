"""
IPT-CITYSPACE
Contrato de Eventos do Atuador da Mesa

Este módulo define a linguagem comum entre:
- pipeline OFFLINE
- simulação virtual
- mesa física real

NÃO contém lógica de controle.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ==============================
# TIPOS DE EVENTO
# ==============================

class ActuatorEventType(Enum):
    MOVE_PIN = "move_pin"
    PIN_REACHED = "pin_reached"
    PHASE_CHANGED = "phase_changed"
    ERROR = "error"


# ==============================
# EVENTO BASE
# ==============================

@dataclass
class ActuatorEvent:
    event_type: ActuatorEventType
    timestamp: float


# ==============================
# EVENTOS ESPECÍFICOS
# ==============================

@dataclass
class MovePinEvent(ActuatorEvent):
    pin_id: int

    x: int              # coluna (0–15)
    y: int              # linha (0–7)

    z_real_m: float     # altura REAL (m)
    z_pin_cm: float     # altura do pino (cm)

    phase: str          # ex: "1940–1959"
    building_name: Optional[str] = None


@dataclass
class PinReachedEvent(ActuatorEvent):
    pin_id: int
    z_pin_cm: float


@dataclass
class PhaseChangedEvent(ActuatorEvent):
    phase: str
    phase_color: str    # ex: "#1f77b4"


@dataclass
class ActuatorErrorEvent(ActuatorEvent):
    message: str
