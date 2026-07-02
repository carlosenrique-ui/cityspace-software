# ==========================================================
# PlanPlayerAdapter (compatível com EventBus)
# ==========================================================

import json
from pathlib import Path


class PlanPlayerAdapter:

    def __init__(self, plan_path, event_bus=None):
        self.plan_path = Path(plan_path)
        self.event_bus = event_bus

        with open(self.plan_path) as f:
            self.plan = json.load(f)

        self.events = self.plan.get("events", [])
        self.index = 0

    # =========================================
    # STEP
    # =========================================
    def step(self):

        if self.index >= len(self.events):
            return None

        event = self.events[self.index]
        self.index += 1

        # opcional: enviar para event_bus
        if self.event_bus:
            try:
                self.event_bus.publish(event)
            except Exception:
                pass

        return event
