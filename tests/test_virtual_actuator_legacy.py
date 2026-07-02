# tests/test_virtual_actuator.py

from runner.virtual_actuator import VirtualActuator


def test_virtual_actuator_records_events():
    """
    Testa se o VirtualActuator registra corretamente
    a sequência de eventos esperada.
    """

    act = VirtualActuator()

    act.reset()
    act.move(row=0, col=0)
    act.set_height_cm(5.0)
    act.reset()

    assert len(act.events) == 4

    assert act.events[0]["type"] == "reset"

    assert act.events[1]["type"] == "move"
    assert act.events[1]["row"] == 0
    assert act.events[1]["col"] == 0

    assert act.events[2]["type"] == "set_height_cm"
    assert act.events[2]["value"] == 5.0

    assert act.events[3]["type"] == "reset"
