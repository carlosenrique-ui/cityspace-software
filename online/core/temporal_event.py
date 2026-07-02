# ==========================================================
# Temporal Event (mínimo necessário para o runtime)
# ==========================================================

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class TemporalEvent:
    event_type: str
    t: Optional[int] = None
    data: Optional[Dict[str, Any]] = None

    def __repr__(self):
        return f"TemporalEvent(type={self.event_type}, t={self.t}, data={self.data})"
