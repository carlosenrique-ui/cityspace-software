# online/ui/visual_adapter.py

class VisualAdapter:
    """
    Adapter entre VisualActuator e UI.
    Não emite eventos, apenas LÊ o estado atual.
    """

    def __init__(self, visual_actuator):
        self.visual = visual_actuator

    def get_pins(self):
        """
        Retorna lista de pinos em formato amigável para UI.
        """
        snapshot = self.visual.snapshot()

        pins = []
        for pin_id, data in snapshot.items():
            pins.append({
                "pin_id": pin_id,
                "x": data["x"],
                "y": data["y"],
                "z_pin_cm": data["z_pin_cm"],
                "phase": data.get("phase"),
            })

        return pins
