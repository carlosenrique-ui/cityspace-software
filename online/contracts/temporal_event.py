from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time


class TemporalEventType(Enum):
    """
    Tipos de eventos que controlam a linha do tempo da simulação.
    """
    PLAY = "play"
    PAUSE = "pause"
    STEP_FORWARD = "step_forward"
    STEP_BACKWARD = "step_backward"
    SEEK = "seek"


@dataclass(frozen=True)
class TemporalEvent:
    """
    Evento temporal enviado pelo UI ou sistema de controle.

    Este contrato é usado pelo EventBus para controlar
    a execução da timeline do sistema.

    Campos:
        event_type : tipo do evento temporal
        t          : posição temporal alvo (usado em SEEK)
        timestamp  : momento em que o evento foi emitido
    """
    event_type: TemporalEventType
    t: Optional[int] = None
    timestamp: float = time.time()