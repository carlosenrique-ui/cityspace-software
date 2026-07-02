# online/core/grid_pin_adapter.py

from online.core.grid_pin_mapper import GridPinMapper
from online.core.actuator_events import MovePinEvent


class GridPinAdapter:
    """
    Adaptador entre eventos lógicos (row, col)
    e drivers físicos (pin_id).
    """

    def __init__(self, mapper: GridPinMapper, driver):
        self.mapper = mapper
        self.driver = driver

    def handle_move_pin(self, event: MovePinEvent):
        """
        Recebe evento MOVE_PIN com row, col, z
        Converte para pin_id e repassa ao driver.
        """

        pin_id = self.mapper.to_pin_id(event.y, event.x)

        self.driver.move_pin(
            pin_id=pin_id,
            height_cm=event.z_pin_cm
        )
