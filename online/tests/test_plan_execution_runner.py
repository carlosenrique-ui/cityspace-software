import json
import os
import tempfile

from online.runtime.plan_execution_runner import PlanExecutionRunner


def test_plan_execution_runner_step_flow():
    plan = [
        {"type": "reset"},
        {"type": "move", "row": 0, "col": 0},
        {"type": "set_height_cm", "value_cm": 5.0},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        plan_path = os.path.join(tmp, "actuator_plan.json")
        with open(plan_path, "w") as f:
            json.dump(plan, f)

        runner = PlanExecutionRunner(plan_path)

        # step 1
        e1 = runner.step()
        assert e1.name == "reset"
        assert runner.current_state is not None

        # step 2
        e2 = runner.step()
        assert e2.name == "move"

        # step 3
        e3 = runner.step()
        assert e3.name == "set_height_cm"

        # fim
        e4 = runner.step()
        assert e4 is None
