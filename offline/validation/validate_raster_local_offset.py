"""
=============================================================
IPT-CitySpace
VALIDAÇÃO – OFFSET UTM → SISTEMA LOCAL CIENTÍFICO
=============================================================

Objetivo:
Determinar o deslocamento necessário para converter
rasters UTM reais para o sistema local científico
utilizado pelo domínio 1:2.

Resultado:
offset_x
offset_y

Esses parâmetros serão utilizados na etapa de
normalização espacial do raster antes da rotação.

Ambiente:
WSL Ubuntu + Conda geo_env_2018
=============================================================
"""

from pathlib import Path
import rasterio
import fiona
from shapely.geometry import shape

# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parents[2]

RASTER_PATH = BASE / "offline/data/processed/dtm/IPT_2018_DTM_UTM23S.tif"

DOMAIN_PATH = BASE / "offline/products/scientific/domain_rect_1x2.gpkg"
DOMAIN_LAYER = "domain_rect_1x2"


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n=================================================")
    print("IPT-CitySpace – OFFSET UTM → LOCAL")
    print("=================================================\n")

    print("[1/3] Lendo raster UTM...")

    with rasterio.open(RASTER_PATH) as src:

        transform = src.transform

        utm_x = transform.c
        utm_y = transform.f

        print(f"Upper Left Raster (UTM): {utm_x:.6f}, {utm_y:.6f}")

    print("\n[2/3] Lendo domínio científico...")

    with fiona.open(DOMAIN_PATH, layer=DOMAIN_LAYER) as src:

        feature = next(iter(src))
        geom = shape(feature["geometry"])

        minx, miny, maxx, maxy = geom.bounds

        print(f"Domínio científico min: {minx:.6f}, {miny:.6f}")

    print("\n[3/3] Calculando offset...")

    offset_x = utm_x - minx
    offset_y = utm_y - miny

    print("\n---------------- RESULTADO ----------------")

    print(f"OFFSET_X = {offset_x:.6f}")
    print(f"OFFSET_Y = {offset_y:.6f}")

    print("-------------------------------------------\n")

    print("✔ Estes valores devem ser aplicados para")
    print("converter raster UTM → sistema científico.\n")


if __name__ == "__main__":
    main()