from pathlib import Path
import shutil
import subprocess

print("\n======================================")
print("CitySpace Context Snapshot Fixer v2")
print("======================================\n")

ROOT = Path(__file__).resolve().parents[2]

CTX = ROOT / "docs/context_snapshot"
CTX.mkdir(parents=True, exist_ok=True)

print("Context directory:", CTX)

# ------------------------------------------------
# artifact extensions to organize
# ------------------------------------------------

EXTENSIONS = [
    ".dot",
    ".svg",
    ".txt",
    ".md"
]

# ------------------------------------------------
# move artifacts generated in project root
# ------------------------------------------------

print("\nScanning project root for artifacts...\n")

for file in ROOT.iterdir():

    if file.is_file():

        if file.suffix in EXTENSIONS:

            dst = CTX / file.name

            if file.parent != CTX:

                print("Moving:", file.name)

                shutil.move(str(file), str(dst))

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
print("Context snapshot organized")
print("Location:", CTX)
print("======================================\n")