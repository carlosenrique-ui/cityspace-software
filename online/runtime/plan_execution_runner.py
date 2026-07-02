# online/runtime/plan_execution_runner.py

from typing import Optional

from online.runtime.plan_player_adapter import PlanPlayerAdapter
from online.core.event_bus import EventBus
from online.core.temporal_conductor import TemporalConductor
from online.core.state_manager import StateManager
from online.core.temporal_event import TemporalEvent


class PlanExecutionRunner:
    """
    Runner ONLINE headless.
    Executa actuator_plan.json passo a passo (step controlado),
    integrando EventBus, TemporalConductor e StateManager.
    """

    def __init__(self, plan_path: str):
        # Infraestrutura central
        self.event_bus = EventBus()

        # Núcleo temporal
        self.temporal_conductor = TemporalConductor(self.event_bus)
        self.state_manager = StateManager(self.event_bus)

        # Player do plano
        self.adapter = PlanPlayerAdapter(
            plan_path=plan_path,
            event_bus=self.event_bus,
        )

        self._last_event: Optional[TemporalEvent] = None

    # --------------------------------------------------
    # Execução STEP
    # --------------------------------------------------

    def step(self) -> Optional[TemporalEvent]:
        """
        Executa UM evento do plano.
        Retorna o TemporalEvent emitido ou None (fim).
        """
        event = self.adapter.step()

        if event is None:
            return None

        # Avança o tempo lógico (1 tick)
        self.temporal_conductor.step()

        self._last_event = event
        return event

    # --------------------------------------------------
    # Estado atual
    # --------------------------------------------------

    @property
    def current_state(self):
        return self.state_manager.current_state

    @property
    def last_event(self) -> Optional[TemporalEvent]:
        return self._last_event
