# ==========================================================
# IPT-CitySpace Offline Pipeline Runner
# ==========================================================

import subprocess
from pathlib import Path

from offline.validation.validate_rotation_pca_grid import run as _rotation_pca_grid_run


PIPELINE_DIR = Path("offline/pipeline")


def _run_pca_alignment_gate() -> None:
    """
    Gate de alinhamento PCA.
    - Bloqueia o pipeline se alignment_status != OK
    - Não bloqueia por historical_delta_status, mas alerta forte
    """
    base_dir = Path(__file__).resolve().parents[1]
    report = _rotation_pca_grid_run(base_dir)

    alignment_status = report.get("status", {}).get("alignment_status")
    historical_delta_status = report.get("status", {}).get("historical_delta_status")

    print("\n================ PCA ALIGNMENT GATE ================")
    print("alignment_status:", alignment_status)
    print("historical_delta_status:", historical_delta_status)

    if historical_delta_status == "CONTRACT-ADDITIVE-REQUIRED":
        print(
            "[WARNING] Delta histórico de rotação divergiu do contrato. "
            "Pipeline seguirá, mas isso exige revisão contratual."
        )

    if alignment_status != "OK":
        raise RuntimeError(
            "Gate de alinhamento PCA bloqueou o pipeline: alignment_status != OK"
        )


def main():

    _run_pca_alignment_gate()

    print("\n===================================")
    print(" IPT-CitySpace OFFLINE PIPELINE ")
    print("===================================\n")

    steps = sorted(PIPELINE_DIR.glob("*.py"))

    for step in steps:

        module = step.with_suffix("").as_posix().replace("/", ".")

        print(f"\nRunning: {module}\n")

        subprocess.run(
            ["python", "-m", module],
            check=True
        )

    print("\nPipeline finished.\n")


if __name__ == "__main__":
    main()
