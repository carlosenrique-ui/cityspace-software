from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class ActuatorCommandType(Enum):
    """
    Tipos de comandos enviados para o sistema de renderização
    ou para o atuador físico da mesa.
    """
    DRAW = "draw"
    ERASE = "erase"
    UPDATE = "update"


@dataclass
class ActuatorCommand:
    """
    Comando de atuação enviado para renderers ou hardware.

    Este contrato é utilizado para desacoplar:
        - renderização
        - simulação
        - controle da mesa física

    Campos:
        type    : tipo do comando
        payload : dados do comando (posição, altura, etc)
        layer   : camada visual ou lógica associada
    """
    type: ActuatorCommandType
    payload: Dict[str, Any]
    layer: str = "default"