class TemporalCoreDirectional:
    """
    Core temporal com direção:
    - Forward (construção)
    - Backward (desconstrução)
    """

    def __init__(self, max_index: int):
        self.running = False
        self.direction = +1
        self.index = 0
        self.max_index = max_index

    # =====================================================
    # CONTROLES
    # =====================================================

    def play_forward(self):
        self.direction = +1
        self.running = True

    def play_backward(self):
        self.direction = -1
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.direction = +1
        self.index = 0
        self.reset_all_pins()

    # =====================================================
    # LOOP TEMPORAL
    # =====================================================

    def tick(self):
        if not self.running:
            return

        new_index = self.index + self.direction

        if 0 <= new_index <= self.max_index:
            self.index = new_index
        else:
            self.running = False

    # =====================================================
    # ACTUATOR (placeholder)
    # =====================================================

    def reset_all_pins(self):
        pass
