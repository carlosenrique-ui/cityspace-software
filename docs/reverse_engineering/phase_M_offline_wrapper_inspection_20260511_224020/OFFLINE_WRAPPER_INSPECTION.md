# Phase M — Offline Wrapper / Delegated Script Inspection

Source Phase L: `docs/reverse_engineering/phase_L_offline_dependency_matrix_20260511_222636`

## Wrapper / delegated scripts inspected

- `offline/pipeline/02_compute_cell_metrics.py`
- `offline/pipeline/03_scientific_to_semantic.py`
- `offline/run_offline_pipeline.py`


## `offline/pipeline/02_compute_cell_metrics.py`

- Exists: `True`
- Has `__main__` guard: `True`
- Functions detected: `0`

### Imports detected
- `from offline.scientific_cell_metrics_utm import main`

### Local script/module candidates
- `offline.scientific_cell_metrics_utm`

### Subprocess calls
- None detected

### runpy calls
- None detected

### os.system calls
- None detected

## `offline/pipeline/03_scientific_to_semantic.py`

- Exists: `True`
- Has `__main__` guard: `True`
- Functions detected: `0`

### Imports detected
- `from offline.adapters.scientific_to_semantic_adapter import main`

### Local script/module candidates
- `offline.adapters.scientific_to_semantic_adapter`

### Subprocess calls
- None detected

### runpy calls
- None detected

### os.system calls
- None detected

## `offline/run_offline_pipeline.py`

- Exists: `True`
- Has `__main__` guard: `True`
- Functions detected: `2`
  - `_run_pca_alignment_gate`
  - `main`

### Imports detected
- `subprocess`
- `from pathlib import Path`
- `from offline.validation.validate_rotation_pca_grid import run`

### Local script/module candidates
- `offline.validation.validate_rotation_pca_grid`

### Subprocess calls
- `run`: `["python", "-m", module], check=True`

### runpy calls
- None detected

### os.system calls
- None detected