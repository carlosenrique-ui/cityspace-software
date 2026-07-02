# online/states/presentation.py

from online.core.state import State


class PresentationState(State):
    def on_entry(self):
        print("[ONLINE] Entrou no estado PRESENTATION")

    def on_event(self, event_type, payload):
        print(f"[PRESENTATION] Evento recebido: {event_type}")
        return None
