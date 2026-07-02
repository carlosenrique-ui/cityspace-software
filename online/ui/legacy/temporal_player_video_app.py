"""
IPT-CITYSPACE
Teste do TemporalConductor com grid OFFLINE real

Objetivo:
- Validar percurso temporal sobre grid real
- Garantir indexação determinística (zig-zag)
- Preparar integração com EventBus e UI
"""

from pathlib import Path

from offline.loading.offline_product import OfflineProduct
from online.core.temporal_conductor import TemporalConductor


def main():
    print("\n=== TESTE TEMPORAL CONDUCTOR COM GRID REAL ===\n")

    snapshot_path = Path(
        "offline/products/snapshots/1cm_rotated"
    )

    product = OfflineProduct(snapshot_path)
    grid = product.grid

    print(f"Grid carregado: shape={grid.shape}")

    conductor = TemporalConductor(
        grid=grid,
        mode="zigzag",
        sleep_sec=0.0
    )

    print("\nPercurso temporal:\n")

    step_count = 0

    for step in conductor.run():
        idx = step["index"]
        i, j = step["ij"]
        z = step["value"]

        print(f"t={idx:03d} | cell=({i},{j}) | Z={z}")
        step_count += 1

    assert step_count == grid.size, "Número de passos não bate com tamanho do grid"

    print("\n✅ TESTE TEMPORAL CONDUCTOR PASSOU\n")


if __name__ == "__main__":
    main()
