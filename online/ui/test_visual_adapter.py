# online/ui/test_visual_adapter.py

from online.core.event_bus import EventBus
from online.core.actuator_events import MovePinEvent
from online.actuators.visual_actuator import VisualActuator
from online.ui.visual_adapter import VisualAdapter


def main():
    bus = EventBus()
    visual = VisualActuator(bus)
    adapter = VisualAdapter(visual)

    # emite dois eventos simulando pinos
    bus.emit(MovePinEvent(
        event_type="MOVE_PIN",
        timestamp=None,
        pin_id=1,
        x=2,
        y=3,
        z_real_m=0.5,
        z_pin_cm=5.0,
        phase="TEST",
    ))

    bus.emit(MovePinEvent(
        event_type="MOVE_PIN",
        timestamp=None,
        pin_id=2,
        x=5,
        y=1,
        z_real_m=1.2,
        z_pin_cm=12.0,
        phase="TEST",
    ))

    pins = adapter.get_pins()

    assert len(pins) == 2
    assert pins[0]["pin_id"] in (1, 2)
    assert "x" in pins[0]
    assert "z_pin_cm" in pins[0]

    print("✔ VisualAdapter OK")


if __name__ == "__main__":
    main()
