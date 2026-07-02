# ==========================================================
# TemporalConductor (compatível com UI + Runner)
# ==========================================================

class TemporalConductor:

    def __init__(self, bus=None, event_bus=None, step_delay_s=0.0, loop=False):
        # compatibilidade com diferentes chamadas
        self.event_bus = bus if bus is not None else event_bus
        self.step_delay_s = step_delay_s
        self.loop = loop

        self.sequence = []
        self.index = 0

    # =========================================
    # LOAD SEQUENCE
    # =========================================
    def load_sequence(self, sequence):
        self.sequence = sequence
        self.index = 0

    # =========================================
    # STEP FORWARD (UI usa isso)
    # =========================================
    def step_forward(self):
        if self.index >= len(self.sequence):
            return None

        state = self.sequence[self.index]
        self.index += 1

        # emitir evento se houver bus
        if self.event_bus:
            try:
                self.event_bus.publish("MOVE_PIN", state)
            except Exception:
                pass

        return state

    # =========================================
    # STEP (compatível com runner)
    # =========================================
    def step(self):
        return self.step_forward()

    # =========================================
    def has_next(self):
        return self.index < len(self.sequence)

    # =========================================
    def reset(self):
        self.index = 0
