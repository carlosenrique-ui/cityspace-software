from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ConstructionFrame:
    """
    Representa o estado da construção urbana em um instante da timeline.

    Cada frame descreve as alterações ocorridas naquele tempo.

    Campos:
        frame_id : identificador único do frame
        t        : posição temporal (ex: ano, passo da simulação)
        created  : elementos criados nesse instante
        removed  : elementos removidos
        updated  : elementos modificados
        metadata : informações adicionais (opcional)
    """
    frame_id: int
    t: int

    created: List[Dict[str, Any]]
    removed: List[Dict[str, Any]]
    updated: List[Dict[str, Any]]

    metadata: Dict[str, Any] | None = None