# IPT-CitySpace Pipeline Execution Flow

## Geospatial Pipeline


DTM
 ↓
gdal_contour
 ↓
noise filtering
 ↓
line densification
 ↓
Chaikin smoothing
 ↓
Method B rotation
 ↓
mesa coordinate conversion
 ↓
cartographic classification
 ↓
GeoPackage
 ↓
Vector tiles

## Entry Point
`engine.py`

### Imports
- argparse
- offline.pipeline_runner
- online.ui.dash_temporal_player
- pathlib
- sys

### Function Calls
- ArgumentParser
- Path
- add_argument
- compile
- exec
- exists
- exit
- fatal
- info
- main
- parse_args
- pipeline
- print
- read_text
- resolve
- run
- run_offline_pipeline
- run_virtual_table_dash
- run_visualization

---


## Entry Point
`offline/pipeline_runner.py`

### Imports
- json
- pathlib
- runner.path
- runner.runner_engine
- runner.virtual_actuator
- typing

### Function Calls
- Path
- RunnerEngine
- VirtualActuator
- dump
- len
- main
- mkdir
- open
- print
- resolve
- run
- run_offline_pipeline
- save_actuator_plan
- zigzag_scan

---


## Entry Point
`offline/scientific_runner.py`

### Imports
- fiona
- pathlib
- shapely.geometry

### Function Calls
- Path
- box
- exists
- len
- main
- mapping
- mkdir
- open
- print
- resolve
- shape
- union
- write

---

