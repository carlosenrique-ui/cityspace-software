from collections import defaultdict
from copy import deepcopy


class VirtualActuator:
    """
    Atuador Virtual
    - Estado determinístico
    - Compatível com Renderer2D
    """

    def __init__(self):
        self.state = defaultdict(int)
        self.history = []

    def execute(self, command):
        before = deepcopy(self.state)

        entity = command.payload

        if command.type.value == "draw":
            self.state[entity] += 1

        elif command.type.value == "erase":
            if entity in self.state:
                self.state[entity] -= 1
                if self.state[entity] <= 0:
                    del self.state[entity]

        elif command.type.value == "update":
            self.state[entity] = 1

        after = deepcopy(self.state)

        self.history.append({
            "command": command,
            "before": before,
            "after": after,
        })

        print(
            f"[VIRTUAL ACTUATOR] {command.type.value.upper()} "
            f"{entity} -> STATE = {dict(self.state)}"
        )

    def snapshot(self):
        return deepcopy(self.state)
