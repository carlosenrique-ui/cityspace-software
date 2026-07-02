import json
from online.runtime.plan_player import PlanPlayer
from runner.virtual_actuator import VirtualActuator


def test_plan_player_executes_plan_correctly():
    plan = [
        {"type": "reset"},
        {"type": "move", "row": 0, "col": 0},
        {"type": "set_height_cm", "value_cm": 1.0},
        {"type": "move", "row": 0, "col": 1},
        {"type": "set_height_cm", "value_cm": 2.0},
        {"type": "reset"},
    ]

    actuator = VirtualActuator()
    player = PlanPlayer(plan, actuator, realtime=False)

    player.play()

    assert len(actuator.events) == 6

    assert actuator.events[0]["type"] == "reset"
    assert actuator.events[1]["type"] == "move"
    assert actuator.events[2]["type"] == "set_height_cm"
    assert actuator.events[3]["type"] == "move"
    assert actuator.events[4]["type"] == "set_height_cm"
    assert actuator.events[5]["type"] == "reset"


def test_plan_player_invalid_plan_type():
    actuator = VirtualActuator()

    try:
        PlanPlayer({"a": 1}, actuator)
        assert False
    except TypeError:
        assert True
