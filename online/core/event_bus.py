class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, handler):
        self._subscribers.setdefault(event_type, []).append(handler)

    def emit(self, event):
        event_type = event.event_type

        if event_type not in self._subscribers:
            return

        for handler in self._subscribers[event_type]:
            handler(event)   # 🔑 PASSA O EVENTO INTEIRO
