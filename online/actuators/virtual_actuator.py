from typing import List, Dict, Any


class VirtualActuator:
    """
    Actuator virtual CANÔNICO.
    Usado por mesa virtual e pelo PlanPlayer.
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def reset(self):
        self.events.append({"type": "reset"})

    def move(self, row: int, col: int):
        self.events.append({
            "type": "move",
            "row": int(row),
            "col": int(col),
        })

    def set_height_cm(self, value: float):
        self.events.append({
            "type": "set_height_cm",
            "value_cm": float(value),
        })
