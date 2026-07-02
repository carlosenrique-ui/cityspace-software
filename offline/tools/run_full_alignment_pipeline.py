"""
IPT-CitySpace
Full Clean Alignment Pipeline
"""

from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parents[2]

PRODUCTS = BASE / "offline/products/scientific"


def run(cmd):
    print("\n>>>", cmd)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("\n❌ ERROR:", cmd)
        sys.exit(1)


def clean_products():
    print("\n==========================================")
    print("Cleaning scientific products (SAFE)...")
    print("==========================================")

    if not PRODUCTS.exists():
        PRODUCTS.mkdir(parents=True, exist_ok=True)
        return

    for item in PRODUCTS.iterdir():

        # 🔥 NÃO APAGAR TRANSFORM
        if item.name.endswith(".json"):
            print(f"Preserving: {item.name}")
            continue

        if item.is_file():
            item.unlink()
        else:
            shutil.rmtree(item)

    print("✔ Clean done.")


def main():

    print("\n==========================================")
    print("IPT-CitySpace – CLEAN PIPELINE")
    print("==========================================")

    # 1️⃣ LIMPA TUDO
    clean_products()

    # 2️⃣ REGERA ENVELOPE (BASE)
    run("python -m offline.tools.desrotate_urban_envelope")

    # 3️⃣ REGERA BUILDINGS
    run("python -m offline.tools.apply_rigid_transform_vector_scientific")

    # 4️⃣ REGERA GRID
    run("python -m offline.scientific_grid_builder")

    print("\n==========================================")
    print("PIPELINE COMPLETED")
    print("==========================================")

    print("\nAgora valide no QGIS:")
    print("- urban_envelope_scientific.gpkg")
    print("- buildings_scientific.gpkg")
    print("- grid_8x16_metric.gpkg")


if __name__ == "__main__":
    main()