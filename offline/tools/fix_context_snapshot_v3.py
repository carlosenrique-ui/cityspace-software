from pathlib import Path
import shutil
import subprocess

print("\n======================================")
print("CitySpace Context Snapshot Fixer v3")
print("======================================\n")

ROOT = Path(__file__).resolve().parents[2]

CTX = ROOT / "docs/context_snapshot"
CTX.mkdir(parents=True, exist_ok=True)

print("Context directory:", CTX)

# ------------------------------------------------
# artifacts expected from context generator
# ------------------------------------------------

ARTIFACTS = [

    "PROJECT_ARCHITECTURE.dot",
    "SCIENTIFIC_PIPELINE.dot",
    "ENGINE_MAP.dot",

    "PROJECT_ARCHITECTURE.svg",
    "SCIENTIFIC_PIPELINE.svg",
    "ENGINE_MAP.svg",

    "IMPORT_MAP.txt",
    "RUNNER_MAP.txt",
    "DATA_FLOW.txt",
    "TODO_MAP.txt"

]

print("\nChecking artifacts in project root...\n")

for name in ARTIFACTS:

    src = ROOT / name
    dst = CTX / name

    if src.exists():

        if src.parent != CTX:

            print("Moving:", name)

            shutil.move(str(src), str(dst))

# ------------------------------------------------
# ensure ENGINE_MAP.dot exists
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
# generate SVG diagrams safely
# ------------------------------------------------

print("\nGenerating SVG diagrams\n")

for dot in CTX.glob("*.dot"):

    svg = dot.with_suffix(".svg")

    print("Generating:", svg.name)

    subprocess.run(
        ["dot", "-Tsvg", str(dot), "-o", str(svg)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

print("\n======================================")
print("Context snapshot organized")
print("Location:", CTX)
print("======================================\n")