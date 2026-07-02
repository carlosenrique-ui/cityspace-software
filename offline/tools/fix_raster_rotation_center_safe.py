from pathlib import Path

print("\n=================================")
print("FIX RASTER ROTATION CENTER (SAFE)")
print("=================================\n")

BASE = Path(__file__).resolve().parents[2]
FILE = BASE / "offline/raster/pipeline/scientific_raster_runner.py"

code = FILE.read_text()

old = 'cx, cy = params["midpoint_original"]'

new = '''
        cx = src.bounds.left + (src.bounds.right - src.bounds.left) / 2
        cy = src.bounds.bottom + (src.bounds.top - src.bounds.bottom) / 2
'''

code = code.replace(old, new)

FILE.write_text(code)

print("Runner corrigido com centro do raster.")
print(FILE)
