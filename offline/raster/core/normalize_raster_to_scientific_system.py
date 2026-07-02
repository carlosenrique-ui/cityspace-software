"""
=============================================================
IPT-CitySpace
NORMALIZAÇÃO RASTER → SISTEMA CIENTÍFICO
=============================================================

Converte raster UTM real para o sistema local científico
utilizado pelo domínio 1:2.

Transformação aplicada:

x_local = x_utm - OFFSET_X
y_local = y_utm - OFFSET_Y

=============================================================
"""

from pathlib import Path
import rasterio
from rasterio.transform import Affine

# ============================================================
# OFFSETS CALCULADOS
# ============================================================

OFFSET_X = 317522.681066
OFFSET_Y = 7394825.317189

# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parents[3]

DTM_UTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_UTM23S.tif"
DSM_UTM = BASE / "offline/data/processed/dsm/IPT_2018_DSM_UTM23S.tif"

DTM_LOCAL = BASE / "offline/data/processed/dtm/IPT_2018_DTM_LOCAL.tif"
DSM_LOCAL = BASE / "offline/data/processed/dsm/IPT_2018_DSM_LOCAL.tif"


# ============================================================
# FUNÇÃO
# ============================================================

def shift_raster(input_path, output_path):

    print("\n=================================================")
    print(f"[SHIFT] {input_path.name}")
    print("=================================================")

    with rasterio.open(input_path) as src:

        data = src.read(1)
        meta = src.meta.copy()

        transform = src.transform

        new_transform = (
            Affine.translation(-OFFSET_X, -OFFSET_Y)
            * transform
        )

        meta.update({
            "transform": new_transform
        })

        with rasterio.open(output_path, "w", **meta) as dst:
            dst.write(data, 1)

    print(f"[OK] Raster convertido para sistema científico")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n=================================================")
    print("IPT-CitySpace – NORMALIZAÇÃO RASTER")
    print("=================================================")

    shift_raster(DTM_UTM, DTM_LOCAL)
    shift_raster(DSM_UTM, DSM_LOCAL)

    print("\n✔ Rasters convertidos para sistema científico\n")


if __name__ == "__main__":
    main()