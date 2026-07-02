"""
===============================================================
IPT-CitySpace
VALIDAÇÃO CIENTÍFICA – TRANSFORMAÇÃO RÍGIDA VETORIAL
===============================================================

Objetivo:
Confirmar que a rotação aplicada preservou área
(transformação rígida sem escala).

Critério:
Área original ≈ Área rotacionada
Erro percentual aceitável < 0.01 %

Implementação:
Sem uso de GeoPandas (evita conflitos Fiona/Numpy)
===============================================================
"""

from pathlib import Path
import fiona
from shapely.geometry import shape

BASE = Path(__file__).resolve().parents[3]

ORIG_PATH = BASE / "offline/products/scientific/urban_envelope_scientific.gpkg"
ROT_PATH  = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

LAYER_ORIG = "urban_envelope_scientific"
LAYER_ROT = "urban_envelope_scientific_rotated_clean"


def read_area(path, layer):

    with fiona.open(path, layer=layer) as src:
        feature = next(iter(src))
        geom = shape(feature["geometry"])
        return geom.area


def main():

    print("\n=================================================")
    print("IPT-CitySpace – VALIDAÇÃO TRANSFORMAÇÃO RÍGIDA")
    print("=================================================\n")

    print("[1/3] Lendo área original...")
    area_orig = read_area(ORIG_PATH, LAYER_ORIG)

    print("[2/3] Lendo área rotacionada...")
    area_rot = read_area(ROT_PATH, LAYER_ROT)

    print("[3/3] Comparando...")

    diff = abs(area_orig - area_rot)
    percent = (diff / area_orig) * 100

    print("\n---------------- RESULTADO ---------------------")
    print(f"Área original      : {area_orig:.6f} m²")
    print(f"Área rotacionada   : {area_rot:.6f} m²")
    print(f"Diferença absoluta : {diff:.6f} m²")
    print(f"Erro percentual    : {percent:.10f} %")
    print("------------------------------------------------\n")

    if percent < 0.01:
        print("✔ TRANSFORMAÇÃO RÍGIDA CONFIRMADA")
        print("✔ Escala preservada")
        print("✔ Sistema permanece em metros reais\n")
    else:
        print("✖ POSSÍVEL ESCALA DETECTADA")
        print("✖ Revisar pipeline de transformação\n")


if __name__ == "__main__":
    main()