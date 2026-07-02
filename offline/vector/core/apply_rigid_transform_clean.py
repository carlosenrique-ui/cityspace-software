"""
===============================================================================
IPT-CitySpace
TRANSFORMAÇÃO RÍGIDA VETORIAL – SISTEMA CIENTÍFICO LOCAL
===============================================================================

CONTEXTO ARQUITETURAL
-------------------------------------------------------------------------------
Este script implementa a transformação rígida que converte o sistema UTM
(EPSG:31983) para o Sistema Científico Local IPT.

Este sistema NÃO é uma reprojeção cartográfica.
É uma transformação geométrica rígida com objetivo operacional.

OBJETIVO DA TRANSFORMAÇÃO
-------------------------------------------------------------------------------
1. Alinhar o urbanismo com o eixo físico da mesa 8x16.
2. Permitir varredura zigzag.
3. Facilitar discretização para grid físico.
4. Manter métrica real (metros).
5. Preservar área e distâncias.

MATEMÁTICA ENVOLVIDA
-------------------------------------------------------------------------------
A transformação aplicada é uma transformação rígida 2D:

1) Rotação em torno de um ponto (cx, cy):

    x' = cx + cos(θ)(x - cx) - sin(θ)(y - cy)
    y' = cy + sin(θ)(x - cx) + cos(θ)(y - cy)

2) Translação:

    x'' = x' + dx
    y'' = y' + dy

Propriedades garantidas:

✔ preserva distâncias
✔ preserva áreas
✔ preserva ângulos
✔ não aplica escala
✔ não aplica deformação

CRÍTICO:
-------------------------------------------------------------------------------
Este sistema deixa de ser UTM absoluto após aplicação da translação.
Portanto:

- CRS declarado como UTM torna-se apenas referencial métrico.
- Coordenadas passam a representar Sistema Local Métrico IPT.
- Este sistema será base para geração do grid 8x16.

CAMADAS DO PROJETO
-------------------------------------------------------------------------------
Camada 1 – IPT_LOCAL_METRIC
    Sistema contínuo métrico em metros.
    Base científica para DTM, DSM, curvas de nível.

Camada 2 – IPT_TABLE_COORD
    Sistema discreto 8x16.
    Origem (0,0) no canto superior esquerdo.
    Eixo Y invertido.
    Conversão final para cm.

IMPORTANTE:
-------------------------------------------------------------------------------
O Sistema Científico NÃO depende da mesa.
A mesa depende do Sistema Científico.

VALIDAÇÃO:
-------------------------------------------------------------------------------
Após execução deste script deve-se executar:

    offline/raster/validation/validate_rigid_transform.py

Para confirmar:

    Área_original ≈ Área_rotacionada
    Erro percentual < 0.01%

===============================================================================
"""
"""
===============================================================================
IPT-CitySpace
TRANSFORMAÇÃO RÍGIDA VETORIAL – VERSÃO DEFINITIVA (SEM GEOPANDAS)
===============================================================================

Aplica rotação + translação preservando área e métrica.

Compatível com Fiona 1.9+
Sem GeoPandas
===============================================================================
"""

import json
from pathlib import Path
import fiona
from shapely.geometry import shape, mapping
from shapely.affinity import rotate, translate

BASE = Path(__file__).resolve().parents[3]

INPUT_PATH = BASE / "offline/products/scientific/urban_envelope_scientific.gpkg"
OUTPUT_PATH = BASE / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"
PARAMS_PATH = BASE / "offline/products/scientific/rigid_transform_params.json"

LAYER_INPUT = "urban_envelope_scientific"
LAYER_OUTPUT = "urban_envelope_scientific_rotated_clean"


def main():

    print("\n=================================================")
    print("IPT-CitySpace – TRANSFORMAÇÃO RÍGIDA DEFINITIVA")
    print("=================================================\n")

    print("[1/5] Lendo parâmetros...")
    with open(PARAMS_PATH) as f:
        params = json.load(f)

    angle = params["theta_rotation_deg"]
    dx = params["dx"]
    dy = params["dy"]
    cx, cy = params["midpoint_original"]

    print(f"Ângulo: {angle}")
    print(f"Centro: ({cx}, {cy})")
    print(f"dx, dy: ({dx}, {dy})")

    print("\n[2/5] Abrindo envelope original...")

    with fiona.open(INPUT_PATH, layer=LAYER_INPUT) as src:

        schema = src.schema
        crs = src.crs

        print("[3/5] Aplicando transformação rígida...")

        with fiona.open(
            OUTPUT_PATH,
            "w",
            driver="GPKG",
            schema=schema,
            crs=crs,
            layer=LAYER_OUTPUT
        ) as dst:

            for feature in src:

                geom = shape(feature["geometry"])

                # Rotação
                geom_rot = rotate(
                    geom,
                    angle,
                    origin=(cx, cy),
                    use_radians=False
                )

                # Translação
                geom_final = translate(
                    geom_rot,
                    xoff=dx,
                    yoff=dy
                )

                new_feature = {
                    "geometry": mapping(geom_final),
                    "properties": feature["properties"]
                }

                dst.write(new_feature)

    print("\n[4/5] Arquivo salvo com sucesso.")
    print(f"Arquivo: {OUTPUT_PATH.name}")

    print("\n[5/5] Transformação concluída.\n")


if __name__ == "__main__":
    main()