from online.core.event_bus import EventBus
from online.core.temporal_state import TemporalState
from online.core.temporal_conductor import TemporalConductor
from online.core.grid_pin_mapper import GridPinMapper
from online.core.grid_pin_adapter import GridPinAdapter
from online.hardware.actuator_driver_mock import ActuatorDriverMock


def test_grid_pin_integration():
    bus = EventBus()

    mapper = GridPinMapper(rows=8, cols=16)
    driver = ActuatorDriverMock()
    adapter = GridPinAdapter(mapper, driver)

    bus.subscribe("MOVE_PIN", adapter.handle_move_pin)

    conductor = TemporalConductor(bus=bus)

    sequence = [
        TemporalState(
            index=0,
            phase="P1",
            x=0,
            y=0,
            z_real_m=0.1,
            z_pin_cm=10.0
        ),
        TemporalState(
            index=1,
            phase="P1",
            x=1,
            y=0,
            z_real_m=0.2,
            z_pin_cm=20.0
        ),
    ]

    conductor.load_sequence(sequence)

    conductor.step_forward()
    conductor.step_forward()

    print("✔ Integração Grid → Pin OK")


if __name__ == "__main__":
    test_grid_pin_integration()
