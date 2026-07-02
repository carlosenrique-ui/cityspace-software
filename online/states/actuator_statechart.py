"""
IPT-CITYSPACE
Statechart do Atuador da Mesa

Controla:
- estados
- transições
- tempo mecânico
- emissão de eventos

NÃO acessa hardware.
"""

import time
from enum import Enum

from online.core.event_bus import EventBus
from online.core.actuator_events import (
    ActuatorEventType,
    MovePinEvent,
    PinReachedEvent,
    ActuatorErrorEvent,
)


# ==============================
# ESTADOS
# ==============================

class ActuatorState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    SETTLING = "settling"
    ERROR = "error"


# ==============================
# STATECHART
# ==============================

class ActuatorStatechart:

    def __init__(
        self,
        event_bus: EventBus,
        move_speed_cm_s: float = 2.0,
        settling_time_s: float = 0.4
    ):
        self.bus = event_bus
        self.state = ActuatorState.IDLE

        self.move_speed = move_speed_cm_s
        self.settling_time = settling_time_s

        self.current_event: MovePinEvent | None = None
        self._t0 = None

        # escuta eventos
        self.bus.subscribe(MovePinEvent, self.on_move_pin)

    # ==========================
    # EVENT HANDLERS
    # ==========================

    def on_move_pin(self, event: MovePinEvent):
        if self.state != ActuatorState.IDLE:
            return  # ignora comandos fora de hora

        self.current_event = event
        self._t0 = time.time()
        self.state = ActuatorState.MOVING

    # ==========================
    # LOOP DE ATUALIZAÇÃO
    # ==========================

    def update(self):
        if self.state == ActuatorState.MOVING:
            self._update_moving()

        elif self.state == ActuatorState.SETTLING:
            self._update_settling()

    # ==========================
    # LÓGICA DE MOVIMENTO
    # ==========================

    def _update_moving(self):
        assert self.current_event is not None

        dz = abs(self.current_event.z_pin_cm)
        t_needed = dz / self.move_speed

        if time.time() - self._t0 >= t_needed:
            self.state = ActuatorState.SETTLING
            self._t0 = time.time()

    def _update_settling(self):
        if time.time() - self._t0 >= self.settling_time:
            evt = PinReachedEvent(
                event_type=ActuatorEventType.PIN_REACHED,
                timestamp=time.time(),
                pin_id=self.current_event.pin_id,
                z_pin_cm=self.current_event.z_pin_cm,
            )

            self.bus.emit(evt)

            self.state = ActuatorState.IDLE
            self.current_event = None
