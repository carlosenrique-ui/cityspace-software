# Phase M2 — Offline Delegated Modules Inspection

Source Phase M: `docs/reverse_engineering/phase_M_offline_wrapper_inspection_20260511_224020`

## Delegated modules resolved

- `offline.adapters.scientific_to_semantic_adapter` → `offline/adapters/scientific_to_semantic_adapter.py` exists=`True`
- `offline.scientific_cell_metrics_utm` → `offline/scientific_cell_metrics_utm.py` exists=`True`
- `offline.validation.validate_rotation_pca_grid` → `offline/validation/validate_rotation_pca_grid.py` exists=`True`

## Runner module string candidates

- None detected

## `offline.adapters.scientific_to_semantic_adapter`

- Path: `offline/adapters/scientific_to_semantic_adapter.py`
- Exists: `True`
- Has `__main__` guard: `True`

### Functions
- `log`
- `main`

### Imports
- `from pathlib import Path`
- `numpy`
- `pandas`
- `json`
- `from offline.config.experiment_config import GRID_ROWS, GRID_COLS, PIN_MAX_CM`

### Read operations
- L51: `df = pd.read_csv(INPUT_CSV)`

### Write operations
- L110: `json.dump(metadata, f, indent=2)`

### Subprocess calls
- None detected

### Module string candidates
- None detected

## `offline.scientific_cell_metrics_utm`

- Path: `offline/scientific_cell_metrics_utm.py`
- Exists: `True`
- Has `__main__` guard: `True`

### Functions
- `main`

### Imports
- `geopandas`
- `rasterio`
- `numpy`
- `pandas`
- `from rasterio.mask import mask`
- `from shapely.geometry import box`

### Read operations
- L14: `gdf = gpd.read_file(GRID, engine="pyogrio")`
- L15: `dsm = rasterio.open(DSM)`
- L16: `dtm = rasterio.open(DTM)`

### Write operations
- L63: `df.to_csv(OUT, index=False)`

### Subprocess calls
- None detected

### Module string candidates
- None detected

## `offline.validation.validate_rotation_pca_grid`

- Path: `offline/validation/validate_rotation_pca_grid.py`
- Exists: `True`
- Has `__main__` guard: `True`

### Functions
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

### Imports
- `from __future__ import annotations`
- `json`
- `math`
- `from pathlib import Path`
- `from typing import Dict, Any`
- `numpy`
- `pandas`
- `from offline.validation.contract_registry import build_contract`

### Read operations
- L162: `df = pd.read_csv(csv_path)`

### Write operations
- L205: `out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")`

### Subprocess calls
- None detected

### Module string candidates
- None detected