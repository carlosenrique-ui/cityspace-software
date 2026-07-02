# Offline Script Classification — IPT CitySpace

## Status

Diagnostic classification only.

No code was modified.

## Classification groups

### 1. Canonical candidates

Files that look like possible official pipeline entrypoints or sequential scientific steps.

See:

`01_canonical_candidates.txt`

### 2. Validation / audit / tests

Files used to validate contracts, CRS, raster alignment, grid dimensions, altitude consistency, PCA/rotation, and tests.

See:

`02_validation_audit_tests.txt`

### 3. Tools / processing / libraries

Reusable processing functions, raster/vector tools, loading utilities, adapters and analysis tools.

See:

`03_tools_processing_libraries.txt`

### 4. Historical / experimental / fix / recompute scripts

Scripts that likely emerged during debugging, correction, recomputation or exploratory development.

See:

`04_historical_experimental_or_fix_scripts.txt`

### 5. Suspect deprecated / backup

Files that require caution before being used as canonical references.

See:

`05_suspect_deprecated_or_backup.txt`

## Architectural interpretation

The Offline layer currently contains:

- candidate canonical pipeline scripts
- validation and contract scripts
- reusable geospatial processing modules
- historical correction/fix/recompute tools
- backups and potentially deprecated files

This confirms the need for a formal canonical pipeline map before any 3D, Cesium, traffic, carbon or physical-table integration.

## Next logical phase

FASE G — Define the canonical OFFLINE execution chain.

This should identify:

1. official entrypoint
2. ordered scientific steps
3. required inputs
4. generated outputs
5. validation gates
6. products consumed by ONLINE/UI
