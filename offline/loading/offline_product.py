# offline/loading/offline_product.py

from pathlib import Path
import json
import numpy as np


class OfflineProduct:
    """
    Produto final do OFFLINE.
    Interface única entre OFFLINE e ONLINE.
    """

    def __init__(self, grid_or_path, metadata=None):

        # Caso 1: Recebe caminho de snapshot
        if isinstance(grid_or_path, (str, Path)):
            snapshot_path = Path(grid_or_path)

            grid_path = snapshot_path / "grid.csv"
            meta_path = snapshot_path / "metadata.json"

            if not grid_path.exists():
                raise FileNotFoundError(f"grid.csv não encontrado em {snapshot_path}")

            # IMPORTANTE: grid usa delimitador ";"
            self.grid = np.loadtxt(grid_path, delimiter=";", dtype=np.uint8)

            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {}

            return

        # Caso 2: Recebe grid direto
        grid = grid_or_path

        if not isinstance(grid, np.ndarray):
            raise TypeError("grid deve ser numpy.ndarray")

        if grid.dtype != np.uint8:
            raise ValueError("grid deve estar normalizado em uint8 (0–255)")

        self.grid = grid
        self.metadata = metadata or {}

    def save(self, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        grid_path = output_dir / "grid.csv"
        meta_path = output_dir / "metadata.json"

        # Salva usando delimitador ";"
        np.savetxt(grid_path, self.grid, fmt="%d", delimiter=";", newline="\n")

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

        print(f"[OfflineProduct] Salvo em: {output_dir}")
