"""
IPT-CitySpace
Validação da Transformação Rígida Aplicada ao Urbanismo

Este script:
- Compara versão original e rotacionada
- Estima ângulo real aplicado
- Estima translação
- Verifica preservação de área
"""

import numpy as np
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point
from math import atan2, degrees


ENGINE_ROOT = Path(__file__).resolve().parents[2]

ORIGINAL_PATH = ENGINE_ROOT / "offline/products/scientific/urban_envelope_original.gpkg"
ROTATED_PATH  = ENGINE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated_clean.gpkg"

LAYER_ORIGINAL = "urban_envelope_original"
LAYER_ROTATED  = "urban_envelope_scientific_rotated_clean"


def get_two_points(gdf):
    """Extrai dois pontos extremos do bounding box"""
    minx, miny, maxx, maxy = gdf.total_bounds
    p1 = np.array([minx, miny])
    p2 = np.array([maxx, maxy])
    return p1, p2


def compute_angle(p1, p2):
    """Calcula ângulo entre dois pontos"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return degrees(atan2(dy, dx))


def main():

    print("="*60)
    print("IPT-CitySpace – VALIDAÇÃO TRANSFORMAÇÃO RÍGIDA")
    print("="*60)

    if not ORIGINAL_PATH.exists():
        print("❌ Arquivo original não encontrado:", ORIGINAL_PATH)
        return

    if not ROTATED_PATH.exists():
        print("❌ Arquivo rotacionado não encontrado:", ROTATED_PATH)
        return

    print("\n[1] Lendo arquivos...")
    gdf_orig = gpd.read_file(ORIGINAL_PATH, layer=LAYER_ORIGINAL)
    gdf_rot  = gpd.read_file(ROTATED_PATH, layer=LAYER_ROTATED)

    print("Original CRS :", gdf_orig.crs)
    print("Rotated CRS  :", gdf_rot.crs)

    print("\n[2] Verificando área...")
    area_orig = gdf_orig.geometry.area.sum()
    area_rot  = gdf_rot.geometry.area.sum()

    print(f"Área original  : {area_orig:.6f}")
    print(f"Área rotacionada: {area_rot:.6f}")
    print(f"Diferença área : {abs(area_orig-area_rot):.6f}")

    print("\n[3] Estimando ângulo aplicado...")

    p1_orig, p2_orig = get_two_points(gdf_orig)
    p1_rot,  p2_rot  = get_two_points(gdf_rot)

    angle_orig = compute_angle(p1_orig, p2_orig)
    angle_rot  = compute_angle(p1_rot, p2_rot)

    angle_aplicado = angle_rot - angle_orig

    print(f"Ângulo original bbox : {angle_orig:.6f}°")
    print(f"Ângulo rotacionado   : {angle_rot:.6f}°")
    print(f"Ângulo estimado      : {angle_aplicado:.6f}°")

    print("\n[4] Estimando translação...")

    centroid_orig = np.array(gdf_orig.geometry.unary_union.centroid.coords[0])
    centroid_rot  = np.array(gdf_rot.geometry.unary_union.centroid.coords[0])

    translation = centroid_rot - centroid_orig

    print(f"Centro original : {centroid_orig}")
    print(f"Centro rotacionado : {centroid_rot}")
    print(f"Translação estimada: dx={translation[0]:.6f}, dy={translation[1]:.6f}")

    print("\n[5] Conclusão")

    if abs(area_orig - area_rot) < 1e-6:
        print("✔ Transformação rígida (área preservada)")
    else:
        print("⚠ Área não preservada — não é transformação rígida pura")

    print("\nValidação concluída.")
    print("="*60)


if __name__ == "__main__":
    main()