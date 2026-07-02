"""
===============================================================================
IPT-CitySpace
SCIENTIFIC RUNNER – FASE 1
Construção do Domínio 1:2 Centrado
===============================================================================

Cria o retângulo fixo 1:2 centrado no envelope científico rotacionado.

Base: IPT_LOCAL_METRIC (metros reais)

Resultado:
offline/products/scientific/domain_rect_1x2.gpkg
===============================================================================
"""

from pathlib import Path
import fiona
from shapely.geometry import shape, mapping, box

# ============================================================================
# BASE DO PROJETO (ipt-cityspace-engine)
# ============================================================================

BASE = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"
OUTPUT_PATH = BASE / "offline/products/scientific/domain_rect_1x2.gpkg"

LAYER_INPUT = "urban_envelope_scientific_rotated_clean"
LAYER_OUTPUT = "domain_rect_1x2"


def main():

    print("\n=================================================")
    print("IPT-CitySpace – SCIENTIFIC RUNNER")
    print("FASE 1 – DOMÍNIO 1:2 CENTRADO")
    print("=================================================\n")

    print("[1/6] Verificando arquivos...")
    print(f"INPUT : {INPUT_PATH}")
    print(f"OUTPUT: {OUTPUT_PATH}\n")

    if not INPUT_PATH.exists():
        print("ERRO: Envelope científico rotacionado não encontrado.")
        return

    print("[2/6] Lendo envelope científico rotacionado...")

    with fiona.open(INPUT_PATH, layer=LAYER_INPUT) as src:
        crs = src.crs
        geometries = [shape(feature["geometry"]) for feature in src]

    print(f"Total de geometrias: {len(geometries)}")

    merged = geometries[0]
    for geom in geometries[1:]:
        merged = merged.union(geom)

    print("[3/6] Calculando bounding box científico...")

    minx, miny, maxx, maxy = merged.bounds

    width = maxx - minx
    height = maxy - miny

    print(f"MinX: {minx:.3f}")
    print(f"MinY: {miny:.3f}")
    print(f"MaxX: {maxx:.3f}")
    print(f"MaxY: {maxy:.3f}")
    print(f"Largura atual: {width:.3f} m")
    print(f"Altura atual : {height:.3f} m\n")

    print("[4/6] Calculando centro geométrico...")

    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2

    print(f"Centro X: {center_x:.3f}")
    print(f"Centro Y: {center_y:.3f}\n")

    print("[5/6] Ajustando para proporção 1:2...")

    target_ratio = 1 / 2  # largura / altura

    current_ratio = width / height

    if current_ratio > target_ratio:
        # Muito largo → aumentar altura
        new_width = width
        new_height = width / target_ratio
        print("Envelope muito largo → aumentando altura")
    else:
        # Muito alto → aumentar largura
        new_height = height
        new_width = height * target_ratio
        print("Envelope muito alto → aumentando largura")

    half_w = new_width / 2
    half_h = new_height / 2

    rect = box(
        center_x - half_w,
        center_y - half_h,
        center_x + half_w,
        center_y + half_h
    )

    print(f"Nova largura: {new_width:.3f} m")
    print(f"Nova altura : {new_height:.3f} m\n")

    print("[6/6] Salvando domínio oficial 1:2...")

    schema = {
        "geometry": "Polygon",
        "properties": {}
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with fiona.open(
        OUTPUT_PATH,
        "w",
        driver="GPKG",
        schema=schema,
        crs=crs,
        layer=LAYER_OUTPUT
    ) as dst:

        dst.write({
            "geometry": mapping(rect),
            "properties": {}
        })

    print("\n✔ Domínio 1:2 criado com sucesso.")
    print(f"Arquivo gerado: {OUTPUT_PATH.name}\n")


if __name__ == "__main__":
    main()