# online/states/analysis.py

from online.core.state import State


class AnalysisState(State):
    def on_entry(self):
        print("[ONLINE] Entrou no estado ANALYSIS")

    def on_event(self, event_type, payload):
        print(f"[ANALYSIS] Evento recebido: {event_type}")
        return None
