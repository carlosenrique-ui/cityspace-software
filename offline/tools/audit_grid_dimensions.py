#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – Grid Dimension Auditor
# ==========================================================

import pandas as pd
import numpy as np
from pathlib import Path

from offline.config.experiment_config import GRID_ROWS, GRID_COLS
from config.system_paths import GRID_METRICS_UTM_CSV

SEMANTIC_GRID = Path(
    "offline/products/snapshots/ipt_fase2_semantic/grid_z_total_m.csv"
)


def audit_scientific_grid():

    print("\n[1] Scientific grid metrics")

    df = pd.read_csv(GRID_METRICS_UTM_CSV)

    rows = df["row"].nunique()
    cols = df["col"].nunique()

    print("rows detected:", rows)
    print("cols detected:", cols)

    expected = GRID_ROWS * GRID_COLS
    actual = len(df)

    print("cells expected:", expected)
    print("cells found:", actual)


def audit_semantic_grid():

    print("\n[2] Semantic mesa grid")

    grid = np.loadtxt(SEMANTIC_GRID, delimiter=";")

    print("shape:", grid.shape)

    min_val = float(np.min(grid))
    max_val = float(np.max(grid))

    print("min:", min_val)
    print("max:", max_val)


def main():

    print("\n==============================================")
    print("IPT-CitySpace – Grid Dimension Audit")
    print("==============================================")

    audit_scientific_grid()
    audit_semantic_grid()

    print("\nAudit finished.")


if __name__ == "__main__":
    main()