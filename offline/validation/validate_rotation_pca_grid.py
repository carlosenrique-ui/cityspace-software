from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd

from offline.validation.contract_registry import build_contract


PCA_ALIGNMENT_TOLERANCE_DEG = 0.5
DELTA_TOLERANCE_DEG = 0.01


def normalize_0_180(angle_deg: float) -> float:
    angle = angle_deg % 180.0
    if angle < 0:
        angle += 180.0
    return angle


def normalize_signed_180(angle_deg: float) -> float:
    angle = angle_deg % 360.0
    if angle > 180.0:
        angle -= 360.0
    if angle <= -180.0:
        angle += 360.0
    return angle


def angle_from_vector(vx: float, vy: float) -> float:
    return normalize_0_180(math.degrees(math.atan2(vy, vx)))


def pca_angle_from_xy(x: np.ndarray, y: np.ndarray) -> float:
    pts = np.column_stack([x, y]).astype(float)

    if pts.shape[0] < 2:
        raise ValueError("Pontos insuficientes para PCA.")

    pts_centered = pts - pts.mean(axis=0, keepdims=True)
    cov = np.cov(pts_centered.T)

    eigvals, eigvecs = np.linalg.eigh(cov)
    principal = eigvecs[:, np.argmax(eigvals)]

    vx = float(principal[0])
    vy = float(principal[1])

    return angle_from_vector(vx, vy)


def compute_grid_fit(pca_angle_deg: float) -> Dict[str, float]:
    pca = normalize_0_180(pca_angle_deg)

    rot_to_x = normalize_signed_180(-pca)
    rot_to_y = normalize_signed_180(90.0 - pca)

    residual_x = abs(normalize_signed_180(pca + rot_to_x))
    residual_y = abs(normalize_signed_180((pca + rot_to_y) - 90.0))

    if abs(rot_to_x) <= abs(rot_to_y):
        best_axis = "x"
        best_rotation = rot_to_x
        best_residual = residual_x
    else:
        best_axis = "y"
        best_rotation = rot_to_y
        best_residual = residual_y

    return {
        "pca_angle_deg": round(pca, 6),
        "rotation_to_align_x_deg": round(rot_to_x, 6),
        "rotation_to_align_y_deg": round(rot_to_y, 6),
        "best_axis": best_axis,
        "best_rotation_deg": round(best_rotation, 6),
        "best_residual_deg": round(best_residual, 6),
    }


def get_rotation_state(contract: Dict[str, Any]) -> Dict[str, Any]:
    geometry = contract.get("geometry", {})
    if "rotation_state" not in geometry:
        raise KeyError("rotation_state não encontrado no contract_registry.py")
    return geometry["rotation_state"]


def compare_with_rotation_state(pca_angle_deg: float, rotation_state: Dict[str, Any]) -> Dict[str, Any]:
    current = rotation_state["current_frame"]
    hist = rotation_state["historical_models"]

    geo = hist["geospatial_alignment"]
    phy = hist["physical_table_fit"]

    computed_delta = round(
        abs(float(geo["source_orientation_deg"]) - float(phy["source_orientation_deg"])),
        6
    )
    contract_delta = float(rotation_state["delta_between_historical_models_deg"])

    return {
        "current_frame": current,
        "comparisons": {
            "pca_vs_current_contract_deg": round(
                normalize_signed_180(pca_angle_deg - float(current["current_pca_deg"])),
                6
            ),
            "pca_vs_geospatial_deg": round(
                normalize_signed_180(pca_angle_deg - float(geo["target_pca_deg"])),
                6
            ),
            "pca_vs_physical_deg": round(
                normalize_signed_180(pca_angle_deg - float(phy["target_pca_deg"])),
                6
            ),
            "geospatial_vs_physical_deg": round(
                normalize_signed_180(float(geo["source_orientation_deg"]) - float(phy["source_orientation_deg"])),
                6
            ),
            "computed_historical_delta_deg": computed_delta,
            "contract_historical_delta_deg": contract_delta,
        },
        "historical_models": hist,
    }


def classify(report: Dict[str, Any]) -> Dict[str, str]:
    current_pca = float(report["pca"]["principal_angle_deg"])
    current_contract = float(report["contract_comparison"]["current_frame"]["current_pca_deg"])
    pca_delta = abs(current_pca - current_contract)

    computed_delta = float(report["contract_comparison"]["comparisons"]["computed_historical_delta_deg"])
    contract_delta = float(report["contract_comparison"]["comparisons"]["contract_historical_delta_deg"])
    delta_diff = abs(computed_delta - contract_delta)

    if pca_delta > PCA_ALIGNMENT_TOLERANCE_DEG:
        alignment_status = "ERROR"
    else:
        alignment_status = "OK"

    if delta_diff > DELTA_TOLERANCE_DEG:
        historical_delta_status = "CONTRACT-ADDITIVE-REQUIRED"
    else:
        historical_delta_status = "OK"

    return {
        "alignment_status": alignment_status,
        "historical_delta_status": historical_delta_status,
    }


def run(base_dir: Path) -> Dict[str, Any]:
    contract = build_contract(base_dir)
    csv_path = Path(contract["paths"]["scientific_grid_csv"])

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV científico não encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    if "x" in df.columns and "y" in df.columns:
        x = df["x"].to_numpy(dtype=float)
        y = df["y"].to_numpy(dtype=float)
        coordinate_source = "scientific_xy"
    elif "col" in df.columns and "row" in df.columns:
        x = df["col"].to_numpy(dtype=float)
        y = df["row"].to_numpy(dtype=float)
        coordinate_source = "grid_row_col_fallback"
    else:
        raise ValueError("Nem x/y nem row/col disponíveis para PCA.")

    pca_angle_deg = pca_angle_from_xy(x, y)
    grid_fit = compute_grid_fit(pca_angle_deg)

    rotation_state = get_rotation_state(contract)
    contract_cmp = compare_with_rotation_state(pca_angle_deg, rotation_state)

    report = {
        "coordinate_source": coordinate_source,
        "tolerances": {
            "pca_alignment_tolerance_deg": PCA_ALIGNMENT_TOLERANCE_DEG,
            "historical_delta_tolerance_deg": DELTA_TOLERANCE_DEG,
        },
        "pca": {
            "principal_angle_deg": round(pca_angle_deg, 6),
        },
        "grid_fit": grid_fit,
        "contract_comparison": contract_cmp,
    }

    report["status"] = classify(report)
    return report


def main() -> int:
    base_dir = Path(".").resolve()
    report = run(base_dir)

    out_dir = base_dir / "offline" / "validation" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "rotation_pca_grid_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n================ ROTATION PCA + GRID FIT ================")
    print("coordinate_source:", report["coordinate_source"])
    print("pca principal angle (deg):", report["pca"]["principal_angle_deg"])
    print("best axis:", report["grid_fit"]["best_axis"])
    print("best rotation (deg):", report["grid_fit"]["best_rotation_deg"])
    print("best residual (deg):", report["grid_fit"]["best_residual_deg"])
    print("contract comparison:", report["contract_comparison"]["comparisons"])
    print("status:", report["status"])
    print("[OK] Report written to:", out_path)

    if report["status"]["alignment_status"] == "ERROR":
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
