# online/runtime/bootstrap_mock.py

from online.core.event_bus import EventBus
from online.core.grid_pin_mapper import GridPinMapper
from online.core.grid_pin_adapter import GridPinAdapter
from online.hardware.actuator_driver_mock import ActuatorDriverMock


def build_runtime():
    bus = EventBus()

    mapper = GridPinMapper(rows=8, cols=16)
    driver = ActuatorDriverMock()

    adapter = GridPinAdapter(mapper, driver)

    bus.subscribe(
        event_type="MOVE_PIN",
        handler=adapter.handle_move_pin
    )

    return bus


if __name__ == "__main__":
    build_runtime()
    print("✔ Runtime MOCK inicializado")
