# IPT-CitySpace
# Reverse Engineering Consolidated Report — Offline A–M2

Generated: 2026-05-11T22:53:11.757433

## Objective

Consolidate the reverse engineering phases executed over the OFFLINE deterministic geospatial pipeline without modifying code or executing the scientific pipeline.

## Methodology

- Static inspection only
- No code modification
- No pipeline execution
- AST inspection
- Import tracing
- IO dependency tracing
- Wrapper/delegation inspection
- Contract-oriented reverse engineering

## Phase Inventory

- Phase A: `docs/reverse_engineering/phase_A_online_20260507_164119`
- Phase B: `docs/reverse_engineering/phase_B_online_contract_20260507_165403`
- Phase C: NOT FOUND
- Phase D: `docs/reverse_engineering/phase_D_offline_20260511_170241`
- Phase E: `docs/reverse_engineering/phase_E_offline_contract_20260511_194745`
- Phase F: `docs/reverse_engineering/phase_F_offline_script_classification_20260511_201700`
- Phase G: `docs/reverse_engineering/phase_G_offline_canonical_chain_20260511_202702`
- Phase H: `docs/reverse_engineering/phase_H_offline_canonical_chain_curated_20260511_203844`
- Phase I: `docs/reverse_engineering/phase_I_offline_canonical_manifest_20260511_205309`
- Phase J: `docs/reverse_engineering/phase_J_offline_manifest_validation_20260511_205935`
- Phase K: `docs/reverse_engineering/phase_K_offline_manifest_io_inspection_20260511_210322`
- Phase K2: `docs/reverse_engineering/phase_K2_offline_manifest_io_inspection_20260511_210803`
- Phase L: `docs/reverse_engineering/phase_L_offline_dependency_matrix_20260511_222636`
- Phase M: `docs/reverse_engineering/phase_M_offline_wrapper_inspection_20260511_224020`
- Phase M2: `docs/reverse_engineering/phase_M2_offline_delegated_modules_20260511_224803`

## Consolidated Findings

### Phase L — Dependency Matrix

- Total scripts inspected: `7`
- Controlled risk scripts: `1`
- Wrapper/delegated scripts: `3`

#### Controlled risk scripts

- `offline/run_offline_pipeline.py`

#### Wrapper/delegated scripts

- `offline/pipeline/02_compute_cell_metrics.py`
- `offline/pipeline/03_scientific_to_semantic.py`
- `offline/run_offline_pipeline.py`

### Phase M2 — Delegated Modules


#### `offline.adapters.scientific_to_semantic_adapter`
- Path: `offline/adapters/scientific_to_semantic_adapter.py`
- Exists: `True`
- Functions:
  - `log`
  - `main`
- Read operations:
  - L51: `df = pd.read_csv(INPUT_CSV)`
- Write operations:
  - L110: `json.dump(metadata, f, indent=2)`

#### `offline.scientific_cell_metrics_utm`
- Path: `offline/scientific_cell_metrics_utm.py`
- Exists: `True`
- Functions:
  - `main`
- Read operations:
  - L14: `gdf = gpd.read_file(GRID, engine="pyogrio")`
  - L15: `dsm = rasterio.open(DSM)`
  - L16: `dtm = rasterio.open(DTM)`
- Write operations:
  - L63: `df.to_csv(OUT, index=False)`

#### `offline.validation.validate_rotation_pca_grid`
- Path: `offline/validation/validate_rotation_pca_grid.py`
- Exists: `True`
- Functions:
  - `normalize_0_180`
  - `normalize_signed_180`
  - `angle_from_vector`
  - `pca_angle_from_xy`
  - `compute_grid_fit`
  - `get_rotation_state`
  - `compare_with_rotation_state`
  - `classify`
  - `run`
  - `main`
- Read operations:
  - L162: `df = pd.read_csv(csv_path)`
- Write operations:
  - L205: `out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")`

## High-Level Offline Architecture

### Scientific pipeline characteristics

- Deterministic
- Sequential
- File-oriented
- Static geospatial processing
- Scientific raster/vector transformations
- Runtime product generation
- Contract-driven validation

### Main scientific responsibilities

- DSM/DTM ingestion
- Grid metrics computation
- Scientific-to-semantic transformation
- PCA rotation validation
- Runtime artifact generation
- CSV/JSON scientific products

### Main geospatial stack detected

- GeoPandas
- Rasterio
- NumPy
- Pandas
- Shapely
- Pyogrio

## Risk Analysis

### Controlled risks

- Wrapper scripts successfully resolved
- No unresolved dynamic module chains detected
- No runpy dynamic execution detected
- Subprocess usage isolated and traceable

### Remaining architectural risks

- Scientific pipeline still depends heavily on file contracts
- Potential hidden runtime assumptions in external datasets
- Sequential dependency chain requires strict artifact consistency

## Final Conclusion

The OFFLINE architecture was successfully reverse engineered through phases A–M2 using only static inspection techniques.
The delegated wrapper structure was resolved and no unresolved dynamic execution chain remains visible after Phase M2.
The resulting documentation now provides a stable architectural baseline for future ONLINE/3D/Twin-City evolution and FAPESP technical reporting.