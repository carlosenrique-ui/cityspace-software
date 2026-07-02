import json
import numpy as np
from pathlib import Path

class TimeEstimator:

    def __init__(self,
                 T_MOVE=0.10,
                 T_Z_MIN=0.08,
                 T_Z_VAR=0.72,
                 H_MAX=0.10,
                 Z_DOWN_FACTOR=0.7):

        self.T_MOVE = T_MOVE
        self.T_Z_MIN = T_Z_MIN
        self.T_Z_VAR = T_Z_VAR
        self.H_MAX = H_MAX
        self.Z_DOWN_FACTOR = Z_DOWN_FACTOR

    def t_up(self, h):
        return self.T_Z_MIN + (h / self.H_MAX) * self.T_Z_VAR

    def t_down(self, h):
        return self.Z_DOWN_FACTOR * self.t_up(h)

    def run(self, plan_path):

        with open(plan_path) as f:
            events = json.load(f)

        total = 0.0
        t_xy = 0.0
        t_up_total = 0.0
        t_down_total = 0.0

        heights = []

        for e in events:

            if e["type"] == "move":
                total += self.T_MOVE
                t_xy += self.T_MOVE

            elif e["type"] == "set_height_cm":

                h = e["value_cm"] / 100.0
                heights.append(h)

                up = self.t_up(h)
                down = self.t_down(h)

                total += up + down
                t_up_total += up
                t_down_total += down

        heights = np.array(heights)

        return {
            "tempo_total_s": total,
            "tempo_total_min": total / 60,
            "tempo_xy_s": t_xy,
            "tempo_up_s": t_up_total,
            "tempo_down_s": t_down_total,
            "altura_media_m": float(heights.mean()),
            "altura_max_m": float(heights.max()),
            "altura_min_m": float(heights.min()),
        }


if __name__ == "__main__":

    plan = Path("products/latest/actuator_plan.json")

    estimator = TimeEstimator()
    result = estimator.run(plan)

    print("\n=== TIME ESTIMATION ===\n")
    for k, v in result.items():
        print(f"{k}: {v}")
