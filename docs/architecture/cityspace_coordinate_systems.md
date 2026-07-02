# IPT-CitySpace Coordinate Systems

This document defines the coordinate systems used in the CitySpace platform.

The system separates scientific processing from the physical table runtime.

---

# CRS-1 — Scientific UTM

Used for all geospatial computations.

Examples:

DSM
DTM
Urban Envelope

Properties:

EPSG:31983
meters
real-world coordinates

Example:

x ≈ 322000
y ≈ 7393000

---

# CRS-2 — Rotated Scientific Domain

Represents the urban model aligned with the physical table orientation.

Properties:

Rigid transformation applied
Still in UTM coordinates

Used for:

urban_envelope_scientific_rotated
z_total_rotated
scientific_grid

---

# CRS-3 — Table Grid

Used by the runtime system.

Coordinates:

row
col

Origin:

top-left corner of the table.

Method:

Method B (CitySpace convention).

Example:

rows = 8
cols = 16

---

# Pipeline Coordinate Flow

UTM (CRS-1)
↓
Rotation
↓
Rotated Domain (CRS-2)
↓
Altimetry Sampling
↓
grid_metrics_utm
↓
Semantic Adapter
↓
Table Grid (CRS-3)
↓
UI / Virtual Table
↓
Physical Table