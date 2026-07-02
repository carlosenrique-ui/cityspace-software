# online/states/initialization.py

from online.core.state import State


class InitializationState(State):
    def on_entry(self):
        print("[ONLINE] Entrou no estado INITIALIZATION")

    def on_event(self, event_type, payload):
        print(f"[INITIALIZATION] Evento recebido: {event_type}")
        return None
