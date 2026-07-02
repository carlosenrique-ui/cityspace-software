# online/core/state.py
"""
Classe base para todos os estados do ONLINE.
"""

from typing import Optional, Any


class State:
    def on_entry(self):
        pass

    def on_exit(self):
        pass

    def on_event(self, event_type: str, payload: Any) -> Optional["State"]:
        return None
