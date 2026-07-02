# Globe-CitySpace
# Provider Discovery Architecture

## Goal

Support any point on Earth.

---

## Terrain Provider Hierarchy

Level A
Municipal IDE

Examples:
- GeoSanja
- Lisboa IDE
- IPT Drone

Level B
Regional IDE

Level C
National IDE

Level D
Copernicus DEM

Level E
SRTM

Level F
Cesium World Terrain

---

## Building Provider Hierarchy

Level A
Municipal Building Registry

Level B
Municipal Footprints

Level C
Microsoft Building Footprints

Level D
Overture Maps

Level E
OpenStreetMap

Level F
Image Based Estimation

---

## Height Fusion Engine

Terrain Provider
        +
Building Provider
        ↓
Height Contract

---

## Examples

GeoSanja Curves
+
Microsoft Footprints

↓

Height Contract

Copernicus DEM
+
OSM Buildings

↓

Height Contract

IPT Drone DSM/DTM
+
IPT Footprints

↓

Height Contract

