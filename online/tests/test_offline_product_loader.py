"""
IPT-CITYSPACE
Teste de integração OFFLINE → ONLINE

Objetivo:
- Validar carregamento de snapshot OFFLINE
- Garantir integridade do grid e metadata
- Servir como ponto de ancoragem para o pipeline ONLINE

Execução:
conda activate geo_env_2018
python -m online.tests.test_offline_product_loader
"""

from pathlib import Path
import numpy as np

from offline.loading.offline_product import OfflineProduct


def main():
    print("\n=== TESTE OFFLINE → ONLINE | OfflineProduct Loader ===\n")

    # Caminho do snapshot OFFLINE
    snapshot_path = Path(
        "offline/products/snapshots/1cm_rotated"
    )

    print(f"Snapshot path: {snapshot_path.resolve()}")

    # Verificações básicas de existência
    assert snapshot_path.exists(), "Snapshot path não existe"
    assert (snapshot_path / "grid.csv").exists(), "grid.csv não encontrado"
    assert (snapshot_path / "metadata.json").exists(), "metadata.json não encontrado"

    # Carregamento do produto OFFLINE
    product = OfflineProduct(snapshot_path)

    print("OfflineProduct instanciado com sucesso.")

    # Grid
    grid = product.grid
    print(f"Grid shape: {grid.shape}")
    print(f"Grid dtype: {grid.dtype}")
    print(f"Grid min / max: {grid.min()} / {grid.max()}")

    # Asserções críticas
    assert isinstance(grid, np.ndarray), "Grid não é numpy array"
    assert grid.shape == (8, 16), "Shape incorreto do grid"
    assert grid.dtype == np.uint8, "Tipo do grid não é uint8"

    # Metadata
    metadata = product.metadata
    print("\nMetadata carregado:")
    for k, v in metadata.items():
        print(f"  {k}: {v}")

    assert "rotation_angle_deg" in metadata, "rotation_angle_deg ausente no metadata"
    assert "grid_shape" in metadata, "grid_shape ausente no metadata"

    print("\n✅ TESTE OFFLINE → ONLINE PASSOU COM SUCESSO\n")


if __name__ == "__main__":
    main()
