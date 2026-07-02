"""
Teste de integração EventBus + StateManager
Usando evento real do sistema (MovePinEvent)
"""

from online.core.event_bus import EventBus
from online.core.state_manager import StateManager
from online.core.state import State
from online.core.actuator_events import MovePinEvent


def test_eventbus_state_manager():
    # ----------------------------
    # Estado dummy observável
    # ----------------------------
    class DummyState(State):
        def __init__(self):
            self.received_events = []

        def on_event(self, event_type, payload):
            print(f"[STATE] recebeu evento {event_type} com {payload}")
            self.received_events.append((event_type, payload))
            return self

    # ----------------------------
    # Infraestrutura
    # ----------------------------
    bus = EventBus()
    manager = StateManager(event_bus=bus)

    # ----------------------------
    # Estado inicial
    # ----------------------------
    initial_state = DummyState()
    initial_state.name = "INITIAL"

    manager.current_state = initial_state
    manager.initialized = True

    print("✔ StateManager pronto")

    # ----------------------------
    # 🔑 ADAPTADOR: EventBus → StateManager
    # ----------------------------
    def state_manager_handler(event):
        manager.handle_event(event.event_type, event)

    bus.subscribe("MOVE_PIN", state_manager_handler)

    print("✔ StateManager inscrito no EventBus para MOVE_PIN")

    # ----------------------------
    # Evento REAL do sistema
    # ----------------------------
    evt = MovePinEvent(
        event_type="MOVE_PIN",
        timestamp=None,
        pin_id=1,
        x=0,
        y=0,
        z_real_m=0.1,
        z_pin_cm=10.0,
        phase="TEST"
    )

    bus.emit(evt)

    print("✔ Evento MOVE_PIN emitido via EventBus")

    # ----------------------------
    # ASSERTS
    # ----------------------------
    assert len(initial_state.received_events) == 1, "Estado não recebeu evento"

    evt_type, payload = initial_state.received_events[0]
    assert evt_type == "MOVE_PIN"
    assert isinstance(payload, MovePinEvent)

    print("✅ TESTE EVENTBUS + STATE MANAGER PASSOU")


if __name__ == "__main__":
    test_eventbus_state_manager()
