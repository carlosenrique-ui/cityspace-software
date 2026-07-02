from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

inject = """
# =========================================
# BUILD GRID FROM EVENTS
# =========================================
import numpy as np

GRID_ROWS = 8
GRID_COLS = 16

def build_grid(events, step):
    grid = np.zeros((GRID_ROWS, GRID_COLS))

    r, c = 0, 0

    for e in events[:step]:
        if e["type"] == "move":
            r = e.get("row", r)
            c = e.get("col", c)

        elif e["type"] == "set_height_cm":
            grid[r][c] = e.get("value_cm", 0)

    return grid
"""

if "def build_grid" not in text:
    text = inject + "\n\n" + text

text = text.replace(
    "z = np.zeros((8, 16))",
    "z = build_grid(ACTUATOR_PLAN, step)"
)

file.write_text(text)

print("✔ PATCH GRID aplicado corretamente")
