#!/usr/bin/env python3
"""
IPT-CitySpace
PIPELINE EXECUTION ORDER BUILDER

Constrói uma ordem lógica de execução do OFFLINE PIPELINE
a partir dos scripts detectados.

Objetivo:
gerar uma lista numerada para organização futura:

01_
02_
03_

Resultado salvo em:

docs/architecture/pipeline_execution_order.txt
"""

from pathlib import Path

print("\n================================================")
print("IPT-CitySpace PIPELINE EXECUTION ORDER BUILDER")
print("================================================\n")

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "docs" / "architecture"
OUTPUT_FILE = OUTPUT_DIR / "pipeline_execution_order.txt"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------
# SCRIPTS DETECTADOS (resultado da etapa anterior)
# ------------------------------------------------

scripts = [

"offline/raster/core/reclip_rasters_to_domain.py",
"offline/raster/core/normalize_raster_to_scientific_system.py",
"offline/raster/pipeline/scientific_raster_runner.py",

"offline/processing/apply_rigid_transform_vector_scientific.py",
"offline/vector/core/apply_rigid_transform_clean.py",
"offline/vector/core/build_domain_1x2_utm.py",

"offline/processing/build_official_urban_envelope_rotated.py",
"offline/processing/dxf_hatch_to_scientific_gpkg_spline.py",

"offline/products/generate_contours_from_dtm.py",
"offline/products/generate_contours_cartographic.py",
"offline/products/generate_contours_cartographic_v2.py",
"offline/products/generate_contours_cartographic_v3.py",
"offline/products/generate_contours_methodB.py",

"offline/products/generate_height_products.py",

"offline/scientific_runner.py",
"offline/scientific_grid_builder.py",
"offline/scientific_cell_metrics.py",
"offline/scientific_cell_metrics_utm.py",

"offline/scanners/zigzag_column_scanner.py",

"offline/adapters/scientific_to_semantic_adapter.py",

"offline/render_dxf_ipt_para_mesa_16x8.py",

"offline/validate_dxf_ipt_original_rotated_clean.py",

"offline/pipeline_runner.py"

]

# ------------------------------------------------
# PRINT
# ------------------------------------------------

print("Scripts in execution order:\n")

for i, s in enumerate(scripts, start=1):

    print(f"{i:02d} -> {s}")

# ------------------------------------------------
# SAVE
# ------------------------------------------------

with open(OUTPUT_FILE, "w") as f:

    f.write("IPT CitySpace Offline Pipeline Order\n\n")

    for i, s in enumerate(scripts, start=1):

        f.write(f"{i:02d} {s}\n")

print("\nExecution order saved:")
print(OUTPUT_FILE)

print("\n================================================")
print("PIPELINE ORDER GENERATED")
print("================================================\n")