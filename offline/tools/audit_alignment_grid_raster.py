#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – Alignment Audit
# Raster × Scientific Grid × Watermark
# ==========================================================

from pathlib import Path
import rasterio
import pandas as pd

ENGINE_ROOT = Path(__file__).resolve().parents[2]

GRID_CSV = ENGINE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

RASTER = ENGINE_ROOT / "offline/products/snapshots/ipt_fase1_1cm/z_total_rotated.tif"

WATERMARK = ENGINE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v53.png"


# ==========================================================
def main():

    print("\n==============================================")
    print("IPT-CitySpace – Alignment Audit")
    print("Raster × Grid × Watermark")
    print("==============================================")

    # ------------------------------------------------------
    # GRID
    # ------------------------------------------------------

    print("\n[1/3] Lendo grid científico...")

    df = pd.read_csv(GRID_CSV)

    xmin = df["x"].min()
    xmax = df["x"].max()
    ymin = df["y"].min()
    ymax = df["y"].max()

    print("Grid bounds:")
    print("xmin:", xmin)
    print("xmax:", xmax)
    print("ymin:", ymin)
    print("ymax:", ymax)

    # ------------------------------------------------------
    # RASTER
    # ------------------------------------------------------

    print("\n[2/3] Lendo raster...")

    with rasterio.open(RASTER) as src:

        bounds = src.bounds

        print("Raster bounds:")
        print("xmin:", bounds.left)
        print("xmax:", bounds.right)
        print("ymin:", bounds.bottom)
        print("ymax:", bounds.top)

    # ------------------------------------------------------
    # COMPARAÇÃO
    # ------------------------------------------------------

    print("\n[3/3] Comparando alinhamento...")

    dx_min = abs(bounds.left - xmin)
    dx_max = abs(bounds.right - xmax)

    dy_min = abs(bounds.bottom - ymin)
    dy_max = abs(bounds.top - ymax)

    print("\nDiferenças:")

    print("xmin:", dx_min)
    print("xmax:", dx_max)
    print("ymin:", dy_min)
    print("ymax:", dy_max)

    tolerance = 0.5

    if dx_min < tolerance and dx_max < tolerance and dy_min < tolerance and dy_max < tolerance:

        print("\n✔ GRID ALINHADO COM RASTER")

    else:

        print("\n⚠ POSSÍVEL DESALINHAMENTO DETECTADO")

    print("\nAudit finalizado.")


# ==========================================================
if __name__ == "__main__":
    main()