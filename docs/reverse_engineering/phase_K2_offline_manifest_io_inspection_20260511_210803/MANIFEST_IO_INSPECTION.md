# Offline Manifest I/O Inspection — FASE K2

## Status
Inspection only.
No pipeline was executed.
No code was modified.
No runner was modified.

## Source manifest
`docs/reverse_engineering/phase_I_offline_canonical_manifest_20260511_205309/offline_canonical_manifest.json`

## Source validation
`docs/reverse_engineering/phase_J_offline_manifest_validation_20260511_205935`

## Manifest top-level keys
- `status`
- `does_execute_pipeline`
- `does_modify_code`
- `does_modify_runner`
- `entrypoint_candidate`
- `validation_gate`
- `canonical_steps`
- `required_online_products`

## Files extracted from manifest
- `offline/pipeline/01_build_scientific_grid.py`
- `offline/pipeline/02_compute_cell_metrics.py`
- `offline/pipeline/02_join_grid_metrics_with_geom.py`
- `offline/pipeline/03_scientific_to_semantic.py`
- `offline/pipeline/04_generate_actuator_plan.py`
- `offline/run_offline_pipeline.py`
- `offline/validation/validate_rotation_pca_grid.py`

## offline/pipeline/01_build_scientific_grid.py
- Exists: True
- Imports found: 2
- Read-like hits: 2
- Write-like hits: 0
- Execution-risk hits: 0
- Product path hits: 2

### Imports
- `geopandas`
- `numpy`

### Read-like operations
- L15: `gdf = gpd.read_file(INPUT_GPKG)`
- L85: `with open(OUTPUT_DEBUG, "w") as f:`

### Write-like operations
_No hits._

### Execution-risk operations
_No hits._

### Product/data path references
- L11: `INPUT_GPKG = "offline/products/scientific/grid_8x16_metric.gpkg"`
- L12: `OUTPUT_DEBUG = "offline/products/scientific/grid_square_debug.txt"`

## offline/pipeline/02_compute_cell_metrics.py
- Exists: True
- Imports found: 1
- Read-like hits: 0
- Write-like hits: 0
- Execution-risk hits: 0
- Product path hits: 0

### Imports
- `offline.scientific_cell_metrics_utm`

### Read-like operations
_No hits._

### Write-like operations
_No hits._

### Execution-risk operations
_No hits._

### Product/data path references
_No hits._

## offline/pipeline/02_join_grid_metrics_with_geom.py
- Exists: True
- Imports found: 3
- Read-like hits: 2
- Write-like hits: 1
- Execution-risk hits: 0
- Product path hits: 1

### Imports
- `geopandas`
- `pandas`
- `pathlib`

### Read-like operations
- L18: `df = pd.read_csv(CSV_PATH)`
- L21: `gdf = gpd.read_file(GPKG_PATH)`

### Write-like operations
- L59: `gdf_merged.to_file(OUT_PATH, driver="GPKG")`

### Execution-risk operations
_No hits._

### Product/data path references
- L8: `BASE = Path("offline/products/scientific")`

## offline/pipeline/03_scientific_to_semantic.py
- Exists: True
- Imports found: 1
- Read-like hits: 0
- Write-like hits: 0
- Execution-risk hits: 0
- Product path hits: 0

### Imports
- `offline.adapters.scientific_to_semantic_adapter`

### Read-like operations
_No hits._

### Write-like operations
_No hits._

### Execution-risk operations
_No hits._

### Product/data path references
_No hits._

## offline/pipeline/04_generate_actuator_plan.py
- Exists: True
- Imports found: 7
- Read-like hits: 2
- Write-like hits: 1
- Execution-risk hits: 0
- Product path hits: 2

### Imports
- `__future__`
- `geopandas`
- `numpy`
- `os`
- `pandas`
- `pathlib`
- `shapely.geometry`

### Read-like operations
- L28: `gdf = gpd.read_file(INPUT_GPKG)`
- L29: `mask = gpd.read_file(MASK_GPKG)`

### Write-like operations
- L106: `df_out.to_csv(OUTPUT_CSV, index=False)`

### Execution-risk operations
_No hits._

### Product/data path references
- L13: `INPUT_GPKG = ENGINE_ROOT / "offline/products/scientific/grid_8x16_enriched.gpkg"`
- L14: `MASK_GPKG = ENGINE_ROOT / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"`

## offline/run_offline_pipeline.py
- Exists: True
- Imports found: 3
- Read-like hits: 0
- Write-like hits: 0
- Execution-risk hits: 1
- Product path hits: 0

### Imports
- `offline.validation.validate_rotation_pca_grid`
- `pathlib`
- `subprocess`

### Read-like operations
_No hits._

### Write-like operations
_No hits._

### Execution-risk operations
- L58: `subprocess.run(`

### Product/data path references
_No hits._

## offline/validation/validate_rotation_pca_grid.py
- Exists: True
- Imports found: 8
- Read-like hits: 1
- Write-like hits: 2
- Execution-risk hits: 0
- Product path hits: 0

### Imports
- `__future__`
- `json`
- `math`
- `numpy`
- `offline.validation.contract_registry`
- `pandas`
- `pathlib`
- `typing`

### Read-like operations
- L162: `df = pd.read_csv(csv_path)`

### Write-like operations
- L203: `out_dir.mkdir(parents=True, exist_ok=True)`
- L205: `out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")`

### Execution-risk operations
_No hits._

### Product/data path references
_No hits._

## Summary
- Total files inspected: 7
- Total read-like hits: 7
- Total write-like hits: 4
- Total execution-risk hits: 1

## Conclusion
FASE K2 successfully inspected static I/O dependencies. Next safe phase: FASE L — dependency matrix.
