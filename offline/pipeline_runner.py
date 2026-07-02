import json
import numpy as np
from pathlib import Path

from runner.runner_engine import RunnerEngine
from runner.virtual_actuator import VirtualActuator
from runner.path import zigzag_scan

# =========================================
# PATHS
# =========================================
BASE = Path("offline/products/runtime")

GRID_PATH = BASE / "grid_cm.npy"
OUTPUT_PATH = BASE / "actuator_plan.json"

# =========================================
# LOAD GRID REAL
# =========================================
if not GRID_PATH.exists():
    raise Exception(f"❌ grid_cm.npy não encontrado: {GRID_PATH}")

grid = np.load(GRID_PATH).tolist()

rows = len(grid)
cols = len(grid[0])

print("========================================")
print("PIPELINE RUNNER – GRID REAL")
print("========================================")
print("Grid:", rows, "x", cols)

# =========================================
# PATH (zigzag)
# =========================================
path = zigzag_scan(cols=cols, rows=rows)

# =========================================
# ACTUATOR
# =========================================
actuator = VirtualActuator()

timing = {
    "move": 0.2,
    "pin": 0.3,
    "hold": 0.1,
}

engine = RunnerEngine(
    grid=grid,
    path=path,
    actuator=actuator,
    timing=timing,
    realtime=False,
)

engine.run()

# =========================================
# SAVE PLAN
# =========================================
plan = {
    "meta": {
        "rows": rows,
        "cols": cols,
        "cell_size_cm": 1,
        "pin_max_cm": 10,
        "generated_by": "pipeline_runner_final",
        "version": "1.0",
    },
    "timing": timing,
    "events": actuator.events,
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(plan, f, indent=2)

print("========================================")
print("✅ ACTUATOR PLAN GERADO")
print("========================================")
