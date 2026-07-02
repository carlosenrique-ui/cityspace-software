from pathlib import Path
import shutil
import subprocess

print("\n======================================")
print("CitySpace Context Snapshot Fixer")
print("======================================\n")

ROOT = Path(__file__).resolve().parents[2]

CTX = ROOT / "docs/context_snapshot"
CTX.mkdir(parents=True, exist_ok=True)

print("Context directory:", CTX)

# ------------------------------------------------
# DOT files expected
# ------------------------------------------------

DOT_FILES = [
    "PROJECT_ARCHITECTURE.dot",
    "SCIENTIFIC_PIPELINE.dot",
    "ENGINE_MAP.dot"
]

# ------------------------------------------------
# move DOT files if they were created in root
# ------------------------------------------------

print("\nChecking DOT files...\n")

for name in DOT_FILES:

    src = ROOT / name
    dst = CTX / name

    if src.exists():

        print("Moving:", src, "->", dst)

        shutil.move(src, dst)

# ------------------------------------------------
# ensure ENGINE_MAP exists
# ------------------------------------------------

engine_dot = CTX / "ENGINE_MAP.dot"

if not engine_dot.exists():

    print("\nENGINE_MAP.dot missing → creating\n")

    engine_dot.write_text(
"""
digraph CitySpaceEngine {

offline_runner -> raster_pipeline
raster_pipeline -> altimetry_model
altimetry_model -> scientific_grid
scientific_grid -> cell_metrics
cell_metrics -> runtime
runtime -> UI
runtime -> physical_table

}
"""
)

# ------------------------------------------------
# generate SVG diagrams
# ------------------------------------------------

print("\nGenerating SVG diagrams\n")

for dot in CTX.glob("*.dot"):

    svg = dot.with_suffix(".svg")

    print("Generating:", svg.name)

    subprocess.run(
        [
            "dot",
            "-Tsvg",
            str(dot),
            "-o",
            str(svg)
        ],
        check=False
    )

print("\n======================================")
print("Context snapshot fixed")
print("Location:", CTX)
print("======================================\n")