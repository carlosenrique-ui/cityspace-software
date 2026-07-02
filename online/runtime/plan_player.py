from typing import Optional
from online.runtime.plan_player_adapter import PlanPlayerAdapter
from online.core.event_bus import EventBus
from online.core.event import Event   # ✅ IMPORT CORRETO


class PlanPlayer:
    """
    Player temporal simples.
    Apenas controla o fluxo (play / pause / step).
    """

    def __init__(self, plan_path: str, bus: EventBus):
        self.bus = bus
        self.adapter = PlanPlayerAdapter(plan_path, bus)
        self._paused = True

    # --------------------------------------------------
    # Controles
    # --------------------------------------------------

    def play(self):
        self._paused = False

    def pause(self):
        self._paused = True

    def reset(self):
        self.adapter.reset()
        self._paused = True

    # --------------------------------------------------
    # Execução
    # --------------------------------------------------

    def step(self) -> Optional[Event]:
        return self.adapter.step()

    def tick(self) -> Optional[Event]:
        if self._paused:
            return None
        return self.step()
