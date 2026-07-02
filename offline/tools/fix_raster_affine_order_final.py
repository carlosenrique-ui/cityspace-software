from pathlib import Path

print("\n===================================")
print("FIX RASTER AFFINE ORDER")
print("===================================\n")

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = FILE.read_text()

code = code.replace(
    "new_transform = T2 * R * T1 * transform",
    "new_transform = T3 * T2 * R * T1 * transform"
)

FILE.write_text(code)

print("Runner corrigido:")
print(FILE)
print("\nOrdem final aplicada:")
print("T3 * T2 * R * T1 * transform\n")
