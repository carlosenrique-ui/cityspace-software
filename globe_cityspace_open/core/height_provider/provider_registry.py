from __future__ import annotations

from pathlib import Path

from .synthetic_provider import SyntheticHeightProvider


def get_height_provider(provider_type: str, spatial_project_path: str | Path):
    if provider_type == "synthetic":
        return SyntheticHeightProvider(spatial_project_path)

    raise ValueError(f"Unknown height provider: {provider_type}")
