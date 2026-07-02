from pathlib import Path

file = Path("online/ui/dash_v50_temporal_truth.py")
text = file.read_text()

# -----------------------------------------
# 1. GARANTIR IMPORT
# -----------------------------------------
if "import numpy as np" not in text:
    text = "import numpy as np\n" + text

# -----------------------------------------
# 2. INSERIR FUNÇÃO build_grid
# -----------------------------------------
if "def build_grid(" not in text:
    inject = """

# =========================================
# BUILD GRID FROM EVENTS
# =========================================
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
    text = inject + "\n" + text

# -----------------------------------------
# 3. SUBSTITUIR GRID ESTÁTICO
# -----------------------------------------
if "np.zeros((8, 16))" in text:
    text = text.replace(
        "np.zeros((8, 16))",
        "build_grid(ACTUATOR_PLAN, step)"
    )

file.write_text(text)

print("✔ FIX COMPLETO APLICADO")
