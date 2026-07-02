"""
=================================================
IPT CitySpace – FIX RASTER AFFINE ORDER
=================================================

Corrige automaticamente a ordem da transformação
Affine no scientific_raster_runner.py
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"


OLD = "new_transform = transform * T1 * R * T2 * T3"
NEW = "new_transform = T3 * T2 * R * T1 * transform"


def main():

    print("\n===================================")
    print("Fixing raster affine order")
    print("===================================\n")

    text = FILE.read_text()

    if OLD not in text:
        print("Linha antiga não encontrada.")
        print("Arquivo talvez já esteja corrigido.")
        return

    text = text.replace(OLD, NEW)

    FILE.write_text(text)

    print("Arquivo corrigido:")
    print(FILE)
    print("\nNova linha aplicada:")
    print(NEW)


if __name__ == "__main__":
    main()