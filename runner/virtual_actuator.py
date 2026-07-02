"""
Virtual Actuator
================

Atuador virtual para simular a mesa de pinos.
Registra eventos para inspeção, testes e geração de actuator_plan.
"""

class VirtualActuator:
    def __init__(self):
        self.events = []

    # -----------------------------
    # Ações básicas
    # -----------------------------

    def reset(self):
        self.events.append({"type": "reset"})

    def move(self, row: int, col: int):
        self.events.append({
            "type": "move",
            "row": row,
            "col": col
        })

    def set_height_cm(self, value: float):
        self.events.append({
            "type": "set_height_cm",
            "value_cm": float(value)
        })

    # -----------------------------
    # Alias semântico (compatibilidade)
    # -----------------------------

    def move_to_cell(self, row: int, col: int):
        """
        Alias semântico usado por testes e players.
        """
        self.move(row=row, col=col)
