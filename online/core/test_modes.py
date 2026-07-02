# online/core/test_modes.py

from online.core.modes import MODES


def test_modes():
    bbox_geo = (-46.70, -23.60, -46.65, -23.55)

    for name, mode in MODES.items():
        grid_profile = mode.build_grid_profile(bbox_geo)

        print(f"\nModo: {name}")
        print(f"  descrição: {mode.description}")
        print(f"  grid: {grid_profile.rows} x {grid_profile.cols}")
        print(f"  cell size: {grid_profile.cell_size_cm} cm")
        print(f"  agregação: {mode.aggregation_policy}")

    print("\n✔ Modes OK")


if __name__ == "__main__":
    test_modes()
