"""
IPT-CitySpace – RECOMPUTE ALTIMETRY (CORRECT v5)

✔ separa terreno / building / total
✔ ignora EMPTY no cálculo de cota zero
✔ remove NODATA corretamente
✔ remove árvores via percentil
✔ mantém arquitetura
✔ logs completos

Autor: Carlos Simoes
"""

from pathlib import Path
import numpy as np
import rasterio

# =========================
# CONFIG
# =========================

BASE = Path(__file__).resolve().parents[2]

DTM_PATH = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
DSM_PATH = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"

OUT_TERRAIN = BASE / "offline/products/grid_terrain_m.csv"
OUT_BUILDING = BASE / "offline/products/grid_building_m.csv"
OUT_TOTAL = BASE / "offline/products/grid_z_total_m.csv"

GRID_ROWS = 8
GRID_COLS = 16

NDSM_THRESHOLD = 2.0
PERCENTILE = 90
NODATA_LIMIT = -1000

# =========================

def print_header():
    print("\n" + "="*60)
    print("IPT-CitySpace – ALTIMETRY (v5 FINAL)")
    print("="*60)


def main():

    print_header()

    # =========================
    # LOAD
    # =========================

    print("\n[1] Loading rasters...")

    with rasterio.open(DTM_PATH) as dtm_ds:
        dtm = dtm_ds.read(1)

    with rasterio.open(DSM_PATH) as dsm_ds:
        dsm = dsm_ds.read(1)

    print("✔ DTM shape:", dtm.shape)
    print("✔ DSM shape:", dsm.shape)

    ndsm = dsm - dtm

    height, width = dtm.shape
    cell_h = height // GRID_ROWS
    cell_w = width // GRID_COLS

    # =========================
    # GRIDS
    # =========================

    grid_terrain = np.full((GRID_ROWS, GRID_COLS), np.nan)
    grid_building = np.zeros((GRID_ROWS, GRID_COLS))
    grid_total = np.full((GRID_ROWS, GRID_COLS), np.nan)

    print("\n[2] Processing cells...\n")

    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):

            y0 = i * cell_h
            y1 = (i + 1) * cell_h
            x0 = j * cell_w
            x1 = (j + 1) * cell_w

            dtm_cell = dtm[y0:y1, x0:x1]
            ndsm_cell = ndsm[y0:y1, x0:x1]

            valid_mask = dtm_cell > NODATA_LIMIT

            if not np.any(valid_mask):
                print(f"[{i:02d},{j:02d}] EMPTY")
                continue

            dtm_valid = dtm_cell[valid_mask]
            ndsm_valid = ndsm_cell[valid_mask]

            # =========================
            # TERRAIN
            # =========================

            z_terrain = float(np.mean(dtm_valid))

            # =========================
            # BUILDING
            # =========================

            building_mask = ndsm_valid > NDSM_THRESHOLD

            if np.any(building_mask):
                z_building = float(
                    np.percentile(ndsm_valid[building_mask], PERCENTILE)
                )
                source = "BUILDING"
            else:
                z_building = 0.0
                source = "TERRAIN"

            z_total = z_terrain + z_building

            grid_terrain[i, j] = z_terrain
            grid_building[i, j] = z_building
            grid_total[i, j] = z_total

            print(
                f"[{i:02d},{j:02d}] {source:<8} "
                f"T={z_terrain:6.2f} "
                f"B={z_building:6.2f} "
                f"Z={z_total:6.2f}"
            )

    # =========================
    # NORMALIZAÇÃO
    # =========================

    print("\n[3] Normalizing to ground zero...")

    min_terrain = np.nanmin(grid_terrain)
    print("✔ Min terrain:", min_terrain)

    grid_terrain -= min_terrain
    grid_total -= min_terrain

    # =========================
    # LIMPEZA FINAL
    # =========================

    grid_terrain = np.nan_to_num(grid_terrain, nan=0.0)
    grid_total = np.nan_to_num(grid_total, nan=0.0)

    # =========================
    # SAVE
    # =========================

    print("\n[4] Saving...")

    np.savetxt(OUT_TERRAIN, grid_terrain, fmt="%.3f", delimiter=";")
    np.savetxt(OUT_BUILDING, grid_building, fmt="%.3f", delimiter=";")
    np.savetxt(OUT_TOTAL, grid_total, fmt="%.3f", delimiter=";")

    print("✔ Terrain:", OUT_TERRAIN)
    print("✔ Building:", OUT_BUILDING)
    print("✔ Total:", OUT_TOTAL)

    print("\n[5] DONE")


if __name__ == "__main__":
    main()