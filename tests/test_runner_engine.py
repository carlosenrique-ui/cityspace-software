from runner.runner_engine import RunnerEngine
from runner.virtual_actuator import VirtualActuator
from runner.path import zigzag_scan


def test_runner_engine_records_expected_sequence():
    """
    Verifica se o RunnerEngine:
    - executa reset inicial
    - percorre o grid
    - aciona move + set_height_cm
    - executa reset final
    """

    # Grid simples 2x2
    grid = [
        [0.1, 0.2],
        [0.3, 0.4],
    ]

    rows = 2
    cols = 2

    path = zigzag_scan(cols=cols, rows=rows)

    actuator = VirtualActuator()

    timing = {
        "move": 0.0,
        "pin": 0.0,
        "hold": 0.0,
    }

    engine = RunnerEngine(
        grid=grid,
        path=path,
        actuator=actuator,
        timing=timing,
        realtime=False,
    )

    engine.run()

    events = actuator.events

    # --------------------------------------------------
    # Verificações estruturais
    # --------------------------------------------------

    # Deve começar e terminar com reset
    assert events[0]["type"] == "reset"
    assert events[-1]["type"] == "reset"

    move_events = [e for e in events if e["type"] == "move"]
    pin_events = [e for e in events if e["type"] == "set_height_cm"]

    assert len(move_events) == rows * cols
    assert len(pin_events) == rows * cols

    # --------------------------------------------------
    # Verificar alturas por célula
    # --------------------------------------------------

    for (row, col), pin_event in zip(path, pin_events):
        assert pin_event["value"] == grid[row][col]


def test_runner_engine_out_of_bounds_returns_zero():
    """
    Células fora do grid devem gerar altura 0.0
    """

    grid = [[1.0]]

    path = [
        (0, 0),
        (1, 0),  # fora do grid
    ]

    actuator = VirtualActuator()

    engine = RunnerEngine(
        grid=grid,
        path=path,
        actuator=actuator,
        timing={"move": 0.0, "pin": 0.0, "hold": 0.0},
        realtime=False,
    )

    engine.run()

    pin_events = [e for e in actuator.events if e["type"] == "set_height_cm"]

    assert pin_events[0]["value"] == 1.0
    assert pin_events[1]["value"] == 0.0
