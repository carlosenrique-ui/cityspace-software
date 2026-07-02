"""
IPT-CITYSPACE
TemporalController

Responsável por:
- Ler snapshot do VisualActuator
- Comparar com frame anterior
- Gerar ConstructionFrame
- Enviar para Renderer2D
"""

from online.contracts.construction_frame import ConstructionFrame


class TemporalController:
    def __init__(self, visual_actuator, renderer):
        self.visual_actuator = visual_actuator
        self.renderer = renderer
        self._last_snapshot = {}

    def tick(self, t: int):
        snapshot = self.visual_actuator.snapshot()

        created = []
        updated = []
        removed = []

        # -------------------------
        # Criações / atualizações
        # -------------------------
        for pin_id, data in snapshot.items():
            entity = ("pin", data["x"], data["y"])

            if pin_id not in self._last_snapshot:
                created.append(entity)
            elif data != self._last_snapshot[pin_id]:
                updated.append(entity)

        # -------------------------
        # Remoções
        # -------------------------
        for pin_id, data in self._last_snapshot.items():
            if pin_id not in snapshot:
                entity = ("pin", data["x"], data["y"])
                removed.append(entity)

        frame = ConstructionFrame(
            t=t,
            created=created,
            updated=updated,
            removed=removed,
        )

        self.renderer.render(frame)
        self._last_snapshot = snapshot
