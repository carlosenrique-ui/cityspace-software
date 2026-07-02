from __future__ import annotations

import json
from pathlib import Path
import argparse

from .provider_registry import get_height_provider


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spatial-project", required=True)
    parser.add_argument("--provider", default="synthetic")
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    provider = get_height_provider(
        args.provider,
        args.spatial_project,
    )

    contract = provider.generate_height_contract()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(contract, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("HEIGHT CONTRACT CREATED")
    print(out)


if __name__ == "__main__":
    main()
