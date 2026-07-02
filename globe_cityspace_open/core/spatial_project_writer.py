from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone


def write_spatial_project(
    output_path: str | Path,
    project_name: str,
    center_lat: float,
    center_lon: float,
    scale: int,
    rows: int = 8,
    cols: int = 16,
    cell_size_cm: int = 2,
    spatial_layout_file: str = "contracts/spatial_layout_16x8.json",
) -> Path:
    """
    Writes the Globe-CitySpace spatial project contract.

    This file is the boundary between:
    - Globe-CitySpace Explorer
    - IPT-CitySpace runtime
    """

    output_path = Path(output_path)

    payload = {
        "contract_type": "spatial_project",
        "contract_version": "G5.2R",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_name": project_name,
        "center": {
            "lat": center_lat,
            "lon": center_lon,
        },
        "scale": scale,
        "grid": {
            "rows": rows,
            "cols": cols,
            "cell_count": rows * cols,
            "cell_size_cm": cell_size_cm,
        },
        "spatial_layout_file": spatial_layout_file,
        "integration_policy": {
            "globe_cityspace_role": "producer_of_spatial_contract",
            "ipt_cityspace_role": "physical_runtime_consumer",
            "direct_import_from_legacy_online_offline": False,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return output_path
