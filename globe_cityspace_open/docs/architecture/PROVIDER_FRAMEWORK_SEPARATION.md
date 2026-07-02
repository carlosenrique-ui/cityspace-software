# Globe-CitySpace
# Provider Framework Separation

## Objective

Separate the data-source architecture into independent provider families:

- Terrain Provider
- Building Provider
- Imagery Provider
- Height Fusion Engine

This prevents city-specific code from contaminating the global architecture.

---

## Universal Principle

The Globe-CitySpace must work for any point on Earth.

A city is only a convenience.

The minimum input is:

- latitude
- longitude
- scale
- grid
- cell size

---

## Provider Families

### Terrain Provider

Produces:

- terrain_height_m

Examples:

- GeoSanja contour terrain provider
- Copernicus DEM provider
- SRTM provider
- Drone DTM provider
- Municipal IDE terrain provider

---

### Building Provider

Produces:

- building_height_m
- building_count
- building_area
- optional footprints

Examples:

- Microsoft Building Footprints
- Overture Maps
- OpenStreetMap
- Municipal building registry
- Drone DSM/DTM derived provider

---

### Imagery Provider

Produces:

- orthophoto
- tile layer
- projected-map background

Examples:

- GeoSanja orthophoto
- OSM
- WMTS
- WMS
- Cesium imagery

---

## Height Fusion Engine

Terrain Provider
+
Building Provider
↓
Height Contract

Formula:

total_height_m = terrain_height_m + building_height_m

Then:

relative_height_m
pin_height_cm
gray_value

---

## Why this matters

São José dos Campos may use:

- GeoSanja contours
- Microsoft footprints
- GeoSanja orthophoto

IPT may use:

- Drone DTM
- Drone DSM
- local footprints

A low-resource city may use:

- Copernicus DEM
- OSM buildings

The pipeline remains the same.
