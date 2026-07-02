# ==========================================================
# StateManager (compatível com EventBus)
# ==========================================================

class StateManager:

    def __init__(self, event_bus=None):
        self.event_bus = event_bus
        self.state = {}

    # =========================================
    # EVENT HANDLER (opcional)
    # =========================================
    def handle_event(self, event):
        # atualização simples de estado
        if hasattr(event, "event_type"):
            self.state["last_event"] = event.event_type

    # =========================================
    # GET STATE
    # =========================================
    def get_state(self):
        return self.state
