"""
CitySpace Scientific Parameters
Central configuration for grid, altimetry and runner
"""

# ===============================
# GRID CONFIGURATION
# ===============================

GRID_ROWS = 8
GRID_COLS = 16

GRID_NAME = f"{GRID_ROWS}x{GRID_COLS}"

# ===============================
# GRID ALIGNMENT
# ===============================
CENTER_URBAN_ON_GRID = True


# ===============================
# GRID ALIGNMENT
# ===============================
CENTER_URBAN_ON_GRID = True


# ===============================
# GRID ALIGNMENT
# ===============================

CENTER_URBAN_ON_GRID = True

# ===============================
# CELL PARAMETERS
# ===============================

CELL_SIZE_METERS = 1.0

# ===============================
# PIN / ACTUATOR PARAMETERS
# ===============================

PIN_HEIGHT_SCALE = 1.0
PIN_MIN_HEIGHT = 0.0
PIN_MAX_HEIGHT = 100.0

# ===============================
# HEIGHT MODEL PARAMETERS
# ===============================

HEIGHT_PERCENTILE_BUILDING = 95
HEIGHT_PERCENTILE_TERRAIN = 10

MIN_BUILDING_FOOTPRINT_RATIO = 0.15

# ===============================
# RUNNER PARAMETERS
# ===============================

FRAME_RATE = 10
SCANNER_SPEED = 1.0

# ROTATION (FIXED)
ROTATION_DEG = 154.63
