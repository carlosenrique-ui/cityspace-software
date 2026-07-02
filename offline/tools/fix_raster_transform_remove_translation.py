from pathlib import Path

print("\n===================================")
print("FIX RASTER TRANSFORM (REMOVE DX/DY)")
print("===================================\n")

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = FILE.read_text()

code = code.replace(
    "T3 = Affine.translation(dx, dy)\n\n        new_transform = T3 * T2 * R * T1 * transform",
    "new_transform = T2 * R * T1 * transform"
)

code = code.replace(
    "T3 * T2 * R * T1 * transform",
    "T2 * R * T1 * transform"
)

FILE.write_text(code)

print("Runner corrigido automaticamente:")
print(FILE)
print("\nDX/DY removidos da transformação raster\n")
