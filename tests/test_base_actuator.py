import pytest
from runner.base_actuator import BaseActuator


def test_base_actuator_is_abstract():
    with pytest.raises(TypeError):
        BaseActuator()
