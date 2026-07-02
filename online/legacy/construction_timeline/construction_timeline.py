# online/time/construction_timeline.py

from online.contracts.construction_frame import ConstructionFrame


class ConstructionTimeline:
    """
    Timeline real de construção:
    - Mantém eventos por tempo
    - Emite ConstructionFrame
    """

    def __init__(self):
        # eventos organizados por tempo
        self._events = {}

    def add_event(self, t: int, action: str, entity):
        """
        action: 'create' | 'remove' | 'update'
        """
        if t not in self._events:
            self._events[t] = []

        self._events[t].append((action, entity))

    def get_frame(self, t: int) -> ConstructionFrame:
        created = []
        removed = []
        updated = []

        events = self._events.get(t, [])

        for action, entity in events:
            if action == "create":
                created.append(entity)
            elif action == "remove":
                removed.append(entity)
            elif action == "update":
                updated.append(entity)

        return ConstructionFrame(
            t=t,
            created=created,
            removed=removed,
            updated=updated
        )
