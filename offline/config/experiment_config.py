"""
IPT-CitySpace – Configuração Experimental Global

Esta camada permite parametrizar o sistema
sem alterar código científico principal.
"""

# ==============================
# GRID CONFIGURATION
# ==============================

GRID_ROWS = 8
GRID_COLS = 16

# ==============================
# PIN / MESA CONFIGURATION
# ==============================

PIN_MAX_CM = 10  # altura máxima física do pino

# ==============================
# TIME CONFIGURATION
# ==============================

TIME_SCALE = 1.0  # 1.0 = tempo real

# ==============================
# SCIENTIFIC OPTIONS
# ==============================

AGGREGATION_METHOD = "mean"   # mean | median | max
NORMALIZATION_METHOD = "linear"