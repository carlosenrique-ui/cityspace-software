# Globe-CitySpace
# BMP Pipeline Architecture

## Objective

Provide a universal pipeline capable of transforming
any point on Earth into a BMP consumable by the physical table.

---

## Universal Flow

Any Point On Earth
        ↓
Coordinate Resolver
        ↓
Spatial Project
        ↓
Provider Discovery Engine
        ↓
Terrain Provider
        +
Building Provider
        ↓
Height Fusion Engine
        ↓
Height Contract
        ↓
Gray Contract
        ↓
BMP Export Engine
        ↓
Physical Table

---

## Input Modes

- Search
- City
- Latitude / Longitude
- Plus Code
- UTM
- Click on Globe
- GeoJSON
- KML
- Shapefile
- Polygon Drawing

---

## Output Modes

- Height Contract
- Gray Contract
- BMP
- PNG
- CSV
- XLSX
- Layer Products
- Virtual Table
- Physical Table

---

## Architectural Principle

The physical table is a consumer of the pipeline.

The physical table must never become the center of the architecture.

