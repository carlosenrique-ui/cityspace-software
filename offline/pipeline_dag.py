# ==========================================================
# IPT-CitySpace – Offline Processing DAG
# ==========================================================

from config.system_paths import (
    GRID_GPKG,
    GRID_METRICS_CSV
)

# ==========================================================
# PIPELINE DE PROCESSAMENTO
# ==========================================================

PIPELINE = [

{
"name": "reproject_rasters",
"script": "offline/processing/reproject_raster.py",

"inputs": [
"offline/data/raw/dtm/*.tif",
"offline/data/raw/dsm/*.tif"
],

"outputs": [
"offline/data/stage1_reproject/dtm/*.tif",
"offline/data/stage1_reproject/dsm/*.tif"
]
},

{
"name": "rotate_rasters",
"script": "offline/raster/core/rotate_raster_scientific.py",

"inputs": [
"offline/data/stage1_reproject/dtm/*.tif",
"offline/data/stage1_reproject/dsm/*.tif"
],

"outputs": [
"offline/data/stage2_rotate/dtm/*.tif",
"offline/data/stage2_rotate/dsm/*.tif"
]
},

{
"name": "clip_domain",
"script": "offline/processing/clip_raster.py",

"inputs": [
"offline/data/stage2_rotate/dtm/*.tif"
],

"outputs": [
"offline/data/stage3_clip/dtm/*.tif"
]
},

{
"name": "normalize_height",
"script": "offline/processing/normalize.py",

"inputs": [
"offline/data/stage3_clip/dtm/*.tif"
],

"outputs": [
"offline/data/stage4_normalize/Z_total.tif"
]
},

{
"name": "build_scientific_grid",
"script": "offline/scientific_grid_builder.py",

"inputs": [
"offline/data/stage4_normalize/Z_total.tif"
],

"outputs": [
f"offline/products/scientific/{GRID_GPKG.name}"
]
},

{
"name": "compute_cell_metrics",
"script": "offline/scientific_cell_metrics_utm.py",

"inputs": [
f"offline/products/scientific/{GRID_GPKG.name}"
],

"outputs": [
f"offline/products/scientific/{GRID_METRICS_CSV.name}"
]
},

{
"name": "generate_pin_heights",
"script": "offline/processing/compute_heights.py",

"inputs": [
f"offline/products/scientific/{GRID_METRICS_CSV.name}"
],

"outputs": [
"offline/products/runtime/grid_pin_heights.csv"
]
},

{
"name": "scanner_path",
"script": "offline/scanners/zigzag_column_scanner.py",

"inputs": [
"offline/products/runtime/grid_pin_heights.csv"
],

"outputs": [
"offline/products/runtime/scanner_sequence.csv"
]
},

{
"name": "export_runtime_frames",
"script": "offline/pipeline_runner_runtime.py",

"inputs": [
"offline/products/runtime/scanner_sequence.csv"
],

"outputs": [
"data/csv_frames/frame_000.csv"
]
}

]

# ==========================================================
# UTILIDADE PARA DEBUG
# ==========================================================

def print_pipeline():

    print("\nCitySpace Pipeline Steps\n")

    for step in PIPELINE:
        print(step["name"])


if __name__ == "__main__":

    print_pipeline()