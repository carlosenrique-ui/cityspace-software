import fiona
from shapely.geometry import shape, box, mapping
from pathlib import Path

# ==========================================================
# IPT-CitySpace – DOMÍNIO 1:2 UTM OFICIAL
# Centralizado e Simétrico
# ==========================================================

BASE = Path(__file__).resolve().parents[3]

INPUT_PATH = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"
INPUT_LAYER = "urban_envelope_scientific_rotated_clean"

OUTPUT_PATH = BASE / "offline/products/scientific/domain_rect_1x2_utm.gpkg"
OUTPUT_LAYER = "domain_rect_1x2_utm"


def main():

    print("\n=================================================")
    print("IPT-CitySpace – DOMÍNIO 1:2 UTM OFICIAL")
    print("=================================================\n")

    print("[1/5] Lendo envelope rotacionado (UTM)...")

    with fiona.open(INPUT_PATH, layer=INPUT_LAYER) as src:
        crs = src.crs
        feature = next(iter(src))
        geom = shape(feature["geometry"])

    minx, miny, maxx, maxy = geom.bounds

    largura = maxx - minx
    altura  = maxy - miny

    print(f"Largura envelope : {largura:.3f} m")
    print(f"Altura envelope  : {altura:.3f} m")

    print("\n[2/5] Calculando centro geométrico...")

    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    print(f"Centro X: {cx:.3f}")
    print(f"Centro Y: {cy:.3f}")

    print("\n[3/5] Ajustando proporção 1:2 (simétrica)...")

    proporcao_atual = altura / largura

    if proporcao_atual < 2:
        # aumentar altura
        nova_altura = largura * 2
        nova_largura = largura
        print("Envelope muito largo → aumentando altura")
    else:
        # aumentar largura
        nova_largura = altura / 2
        nova_altura = altura
        print("Envelope muito alto → aumentando largura")

    print(f"Nova largura : {nova_largura:.3f} m")
    print(f"Nova altura  : {nova_altura:.3f} m")

    print("\n[4/5] Construindo domínio 1:2...")

    new_minx = cx - nova_largura / 2
    new_maxx = cx + nova_largura / 2
    new_miny = cy - nova_altura / 2
    new_maxy = cy + nova_altura / 2

    domain = box(new_minx, new_miny, new_maxx, new_maxy)

    if OUTPUT_PATH.exists():
        OUTPUT_PATH.unlink()

    schema = {
        "geometry": "Polygon",
        "properties": {}
    }

    with fiona.open(
        OUTPUT_PATH,
        mode="w",
        driver="GPKG",
        schema=schema,
        crs=crs,
        layer=OUTPUT_LAYER,
    ) as dst:
        dst.write({
            "geometry": mapping(domain),
            "properties": {}
        })

    print("\n[5/5] Finalizado.")
    print("✔ Domínio 1:2 UTM criado com sucesso.")
    print(f"Arquivo: {OUTPUT_PATH.name}\n")


if __name__ == "__main__":
    main()