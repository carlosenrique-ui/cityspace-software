# online/states/online_root.py
from online.core.state import State


class OnlineRootState(State):
    def on_entry(self):
        print("[ONLINE] Entrou no estado raiz")

    def on_event(self, event_type, payload):
        print(f"[ONLINE] Evento recebido no root: {event_type}")
        return None
