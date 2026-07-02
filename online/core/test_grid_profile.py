# online/core/test_grid_profile.py

from online.core.grid_profile import GridProfile


def test_grid_profile():
    profile = GridProfile(
        rows=8,
        cols=16,
        cell_size_cm=1.0,  # modo BAIRRO
        bbox_geo=(-46.70, -23.60, -46.65, -23.55)
    )

    # -----------------------------
    # Teste físico
    # -----------------------------
    X, Y = profile.pin_to_physical_cm(0, 0)
    assert (X, Y) == (0.0, 0.0)

    X, Y = profile.pin_to_physical_cm(15, 7)
    assert X == 15.0
    assert Y == 7.0

    # -----------------------------
    # Teste geográfico
    # -----------------------------
    lon, lat = profile.pin_to_geo(0, 0)
    print("Topo direito:", lon, lat)

    lon, lat = profile.pin_to_geo(15, 7)
    print("Inferior esquerdo:", lon, lat)

    print("✔ GridProfile OK")


if __name__ == "__main__":
    test_grid_profile()
