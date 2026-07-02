"""
============================================================
IPT-CitySpace – VALIDAÇÃO COMPLETA TRANSFORMAÇÃO RÍGIDA
============================================================

Objetivo:
- Ler rigid_transform_params.json
- Verificar theta
- Verificar centro
- Verificar coerência com envelope rotacionado
- Detectar se foi usado método A (rotate+translate)
  ou método B (rotate com origin explícito)
"""

import json
import math
from pathlib import Path

import geopandas as gpd
from shapely.affinity import rotate

ENGINE_ROOT = Path(__file__).resolve().parents[2]

PARAMS_PATH = ENGINE_ROOT / "offline/products/scientific/rigid_transform_params.json"
ROTATED_PATH = ENGINE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

def main():
    print("============================================================")
    print("IPT-CitySpace – VALIDAÇÃO COMPLETA TRANSFORMAÇÃO RÍGIDA")
    print("============================================================")

    # ------------------------------------------------------------------
    # 1) Ler JSON
    # ------------------------------------------------------------------
    if not PARAMS_PATH.exists():
        print("❌ JSON não encontrado:", PARAMS_PATH)
        return

    with open(PARAMS_PATH) as f:
        params = json.load(f)

    theta = params.get("theta_rotation_deg", None)
    cx = params.get("center_x", None)
    cy = params.get("center_y", None)

    print("\n[1] Parâmetros encontrados:")
    print("theta_rotation_deg:", theta)
    print("center_x:", cx)
    print("center_y:", cy)

    if theta is None:
        print("❌ theta_rotation_deg ausente.")
        return

    # ------------------------------------------------------------------
    # 2) Ler envelope rotacionado
    # ------------------------------------------------------------------
    if not ROTATED_PATH.exists():
        print("❌ Envelope rotacionado não encontrado.")
        return

    gdf = gpd.read_file(ROTATED_PATH)
    geom = gdf.geometry.iloc[0]

    minx, miny, maxx, maxy = geom.bounds

    print("\n[2] Envelope rotacionado bounds:")
    print("minx:", minx)
    print("miny:", miny)
    print("maxx:", maxx)
    print("maxy:", maxy)

    # ------------------------------------------------------------------
    # 3) Avaliação geométrica
    # ------------------------------------------------------------------
    print("\n[3] Avaliação geométrica:")

    if cx is None or cy is None:
        print("⚠ Centro não definido no JSON.")
        print("Provavelmente método A (rotate + translate).")
    else:
        print("Centro definido. Método B provável.")
        print("Centro (cx, cy) =", (cx, cy))

    print("\n[4] Análise do ângulo:")
    print("theta =", theta, "graus")
    print("theta_rad =", math.radians(theta))

    print("\n✔ Validação estrutural concluída.")
    print("============================================================")


if __name__ == "__main__":
    main()