from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"


OLD = "new_transform = T3 * T2 * R * T1 * transform"

NEW = """
# transformação correta: rotate → translate → rotate
R1 = Affine.rotation(angle)
T  = Affine.translation(dx, dy)
R2 = Affine.rotation(-angle)

new_transform = transform * R1 * T * R2
"""


def main():

    print("\nFixing scientific raster transform\n")

    text = FILE.read_text()

    if OLD not in text:
        print("Transform line not found")
        return

    text = text.replace(OLD, NEW)

    FILE.write_text(text)

    print("File patched:")
    print(FILE)


if __name__ == "__main__":
    main()