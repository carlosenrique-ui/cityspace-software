"""
IPT-CitySpace
Validação Formal dos Parâmetros de Transformação Rígida

Este script:
- Lê rigid_transform_params.json
- Valida parâmetros obrigatórios
- Constrói matriz rígida oficial
- Verifica ortogonalidade
- Verifica determinante
- Formaliza sistema científico
"""

import json
import numpy as np
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[2]
PARAMS_PATH = ENGINE_ROOT / "offline/products/scientific/rigid_transform_params.json"


def build_rotation_matrix(theta_deg):
    theta_rad = np.radians(theta_deg)
    cos_t = np.cos(theta_rad)
    sin_t = np.sin(theta_rad)

    R = np.array([
        [cos_t, -sin_t],
        [sin_t,  cos_t]
    ])

    return R


def main():

    print("="*60)
    print("IPT-CitySpace – VALIDAÇÃO RIGID_TRANSFORM_PARAMS.JSON")
    print("="*60)

    if not PARAMS_PATH.exists():
        print("❌ Arquivo não encontrado:", PARAMS_PATH)
        return

    print("\n[1] Lendo parâmetros...")
    with open(PARAMS_PATH) as f:
        params = json.load(f)

    required_keys = [
        "theta_rotation_deg",
        "center_x",
        "center_y",
        "dx",
        "dy"
    ]

    missing = [k for k in required_keys if k not in params]
    if missing:
        print("❌ Parâmetros ausentes:", missing)
        return

    theta = float(params["theta_rotation_deg"])
    cx = float(params["center_x"])
    cy = float(params["center_y"])
    dx = float(params["dx"])
    dy = float(params["dy"])

    print(f"Ângulo (deg): {theta}")
    print(f"Centro: ({cx}, {cy})")
    print(f"Translação: dx={dx}, dy={dy}")

    print("\n[2] Construindo matriz de rotação...")
    R = build_rotation_matrix(theta)

    print("Matriz R:")
    print(R)

    print("\n[3] Verificando ortogonalidade (RᵀR)...")
    RtR = R.T @ R
    print(RtR)

    identity = np.eye(2)
    error = np.linalg.norm(RtR - identity)

    print(f"Erro ortogonalidade: {error:.12f}")

    if error < 1e-10:
        print("✔ Matriz ortogonal válida")
    else:
        print("⚠ Matriz NÃO é ortogonal")

    print("\n[4] Verificando determinante...")
    det = np.linalg.det(R)
    print(f"Determinante: {det:.12f}")

    if abs(det - 1.0) < 1e-10:
        print("✔ Determinante = 1 (transformação rígida pura)")
    else:
        print("⚠ Determinante diferente de 1")

    print("\n[5] Matriz Afim Completa (3x3)")

    affine = np.array([
        [R[0,0], R[0,1], dx],
        [R[1,0], R[1,1], dy],
        [0,       0,      1]
    ])

    print(affine)

    print("\nSistema Científico Oficial:")
    print("Sistema = UTM23S + Transformação rígida consolidada")
    print("="*60)


if __name__ == "__main__":
    main()