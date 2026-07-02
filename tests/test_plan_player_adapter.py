import json
import os
import tempfile

from online.runtime.plan_player_adapter import PlanPlayerAdapter
from online.core.event_bus import EventBus
from online.contracts.temporal_event import TemporalEvent


def test_plan_player_adapter_emits_events():
    # --------------------------------------------------
    # Criar actuator_plan.json temporário
    # --------------------------------------------------
    plan = [
        {"type": "reset"},
        {"type": "move", "row": 0, "col": 0},
        {"type": "set_height_cm", "value_cm": 5.0},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        plan_path = os.path.join(tmp, "actuator_plan.json")

        with open(plan_path, "w") as f:
            json.dump(plan, f)

        # --------------------------------------------------
        # EventBus REAL
        # --------------------------------------------------
        bus = EventBus()
        received = []

        def handler(event: TemporalEvent):
            received.append(event)

        bus.subscribe("reset", handler)
        bus.subscribe("move", handler)
        bus.subscribe("set_height_cm", handler)

        # --------------------------------------------------
        # Adapter
        # --------------------------------------------------
        adapter = PlanPlayerAdapter(plan_path, bus)

        # step 1
        e1 = adapter.step()
        assert e1.event_type == "reset"

        # step 2
        e2 = adapter.step()
        assert e2.event_type == "move"
        assert e2.t["row"] == 0
        assert e2.t["col"] == 0

        # step 3
        e3 = adapter.step()
        assert e3.event_type == "set_height_cm"
        assert e3.t["value"] == 5.0

        # fim
        e4 = adapter.step()
        assert e4 is None

        # --------------------------------------------------
        # Verificações do EventBus
        # --------------------------------------------------
        assert len(received) == 3
        assert received[0].event_type == "reset"
        assert received[1].event_type == "move"
        assert received[2].event_type == "set_height_cm"
