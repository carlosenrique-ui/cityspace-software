from pathlib import Path

print("\n=================================")
print("FIX RASTER ROTATION CENTER")
print("=================================\n")

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = FILE.read_text()

code = code.replace(
    "cx, cy = params[\"midpoint_original\"]",
    "cx = src.bounds.left + (src.bounds.right - src.bounds.left) / 2\n        cy = src.bounds.bottom + (src.bounds.top - src.bounds.bottom) / 2"
)

FILE.write_text(code)

print("Runner atualizado:")
print(FILE)
print("\nCentro de rotação agora é o centro do raster\n")
