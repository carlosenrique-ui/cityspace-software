# Globe-CitySpace Engineering Handbook

---

# Chapter 06 — Offline Scientific Pipeline

## 1. Purpose

This chapter describes the complete scientific processing pipeline executed during the Offline (Explorer) phase.

The objective of the Offline Pipeline is to transform geographic information into deterministic engineering products that can later be consumed by IPT-CitySpace, the Virtual Table and the Physical Table.

The Offline Pipeline performs all computationally intensive scientific operations before real-time interaction begins.

---

## 2. General Architecture

The Offline Pipeline consists of four major stages:

1. Geographic Exploration

2. Scientific Processing

3. Product Generation

4. Export

Only validated scientific products are transferred to the operational environment.

---

## 3. Pipeline Overview

The complete workflow is illustrated below.

```text
Latitude / Longitude

↓

Globe Navigation

↓

Area Exploration

↓

Project Rotation

↓

Bounding Box

↓

Scientific Grid

↓

Terrain Processing

↓

Building Processing

↓

Scientific Height Model

↓

Raster Generation

↓

Scientific Products

↓

Metadata

↓

Validation

↓

Export
```

Every execution follows exactly the same deterministic sequence.

---

## 4. Geographic Exploration

The exploration phase allows the user to investigate any region of the planet.

Available operations include:

- Zoom
- Pan
- Rotation
- Camera positioning
- Layer visualization
- Dataset selection

No scientific processing occurs during this stage.

---

## 5. Project Definition

A project begins when the user defines:

- Latitude
- Longitude
- Project centroid
- Area dimensions
- Grid dimensions
- Resolution

These parameters uniquely identify a scientific project.

---

## 6. Project Rotation

The exploration interface allows the user to rotate the project before scientific processing begins.

The selected angle defines the engineering reference frame used by the entire project.

Rotation is performed around the project centroid.

```
Rotation Center = Project Centroid
```

This angle becomes a permanent scientific parameter.

It shall be stored in the project metadata.

Examples include:

- aligning a road with the X axis;
- aligning an airport runway;
- aligning an urban corridor;
- aligning an industrial complex.

Once accepted, the same angle is applied consistently throughout the complete Offline Pipeline.

---

## 7. Bounding Box

After the centroid and rotation are defined, the system computes the project Bounding Box.

The Bounding Box defines:

- West
- East
- South
- North

These limits determine the scientific area to be processed.

---

## 8. Scientific Grid

A regular grid is generated over the rotated project area.

Each cell stores:

- Row
- Column
- Latitude
- Longitude
- UTM coordinates
- Terrain height
- Building height
- Total height

The grid becomes the primary scientific sampling structure.

---

## 9. Coordinate Transformation

Scientific calculations require projected coordinates.

The workflow is:

```text
EPSG:4326

↓

Automatic CRS Selection

↓

UTM Projection

↓

Metric Processing
```

All distance, area and grid calculations are performed in projected coordinates.

Latitude and longitude remain preserved for navigation.

---

## 10. Terrain Processing

The terrain subsystem loads the selected Digital Terrain Model (DTM).

Typical sources include:

- FABDEM
- Copernicus DEM
- SRTM
- Municipal DTM
- LiDAR-derived terrain

Terrain elevation is interpolated to each scientific grid cell.

Each cell receives:

```
Zterrain
```

representing the bare-earth elevation.

---

## 11. Building Processing

Buildings are processed independently from terrain.

Possible data sources include:

- Municipal GIS
- OpenStreetMap
- Overture Maps
- Global Building Atlas
- Microsoft Building Footprints

Each building contributes:

```
Zbuilding
```

representing the elevation above terrain.

When only footprints exist, configurable height estimation may be applied.

---

## 12. Scientific Height Model

The scientific model computes:

```
Ztotal = Zterrain + Zbuilding
```

Three independent products are preserved:

- Terrain Model
- Building Model
- Total Height Model

This separation guarantees scientific traceability.

---

## 13. Scientific Sampling

Each grid cell samples the underlying geographic information.

Typical attributes include:

- Mean terrain elevation
- Maximum terrain elevation
- Building height
- Occupancy
- Surface classification

Sampling algorithms are deterministic.

Repeated execution over identical datasets produces identical values.

---

## 14. Height Normalization

Scientific heights are normalized for visualization and actuator control.

Normalization generates:

- Floating-point heights
- Grayscale values
- Pin heights

The normalization process never modifies the original scientific data.

Original elevations remain available in the metadata and CSV products.

---

## 15. Scientific Validation

Before export, the scientific model verifies:

- CRS consistency
- Rotation consistency
- Grid completeness
- Missing values
- Height ranges
- Raster dimensions

Invalid projects are rejected before product generation.

---

## 16. Rotation Consistency

The Project Rotation Angle shall be applied identically to:

- Scientific Grid
- Raster generation
- Projection image
- Height image
- CSV coordinates
- Metadata
- Virtual Table
- Physical Table

No subsystem may redefine or modify the project rotation after scientific processing begins.

The project reference frame is established only once during the exploration phase.

---

## 17. Raster Generation

After scientific processing, raster products are generated.

The primary raster layers include:

- Terrain Raster
- Building Raster
- Total Height Raster
- Projection Raster
- Gray Level Raster

All rasters inherit the Project Rotation Angle and preserve the scientific reference frame.

---

## 18. BMP Generation

Bitmap products are generated for visualization and projection mapping.

Typical outputs include:

- projection_top.bmp
- heightmap.bmp
- grayscale.bmp
- occupancy.bmp

The BMP files preserve:

- Project rotation
- Grid alignment
- Scientific sampling
- Pixel-to-cell correspondence

These products are optimized for high-speed rendering.

---

## 19. CSV Generation

Structured CSV products are exported for validation and interoperability.

Typical files include:

- grid_metrics_utm.csv
- grid_height.csv
- grid_uint8.csv
- grid_pino_cm.csv
- grid_terrain_m.csv
- grid_building_m.csv

Each CSV row corresponds to one scientific grid cell.

Typical attributes include:

- Row
- Column
- Latitude
- Longitude
- UTM Easting
- UTM Northing
- Terrain Height
- Building Height
- Total Height
- Gray Level
- Pin Height

---

## 20. Metadata Generation

Each project automatically generates metadata describing the complete processing session.

Metadata include:

- Project name
- Processing date
- Software version
- CRS
- Grid dimensions
- Cell size
- Project centroid
- Bounding Box
- Project Rotation Angle
- Data sources
- Processing parameters

Metadata are exported in JSON format.

---

## 21. Scientific Products

The Offline Pipeline generates all products required by the operational environment.

Typical outputs include:

```text
projection_top.bmp

heightmap.bmp

grid_metrics_utm.csv

grid_height.csv

grid_uint8.csv

grid_pino_cm.csv

grid.npy

metadata.json

actuator_plan.json
```

These files represent the complete scientific description of the processed project.

---

## 22. Deterministic Processing

The Offline Pipeline is deterministic.

Given:

- identical datasets;
- identical centroid;
- identical rotation angle;
- identical grid dimensions;
- identical software version;

the generated outputs shall always be identical.

This guarantees reproducibility for scientific publications, engineering validation and long-term project maintenance.

---

## 23. Export Validation

Before export, every generated product is validated.

Validation includes:

- File existence
- File dimensions
- CRS consistency
- Grid consistency
- Rotation consistency
- Metadata completeness
- Height range verification
- Product integrity

Only validated products may proceed to the operational environment.

---

## 24. Export to the Virtual Table

The Virtual Table receives the scientific products generated by the Offline Pipeline.

Transferred products include:

- Projection BMP
- Height BMP
- Grid CSV
- Metadata
- Actuator plan

The Virtual Table reproduces exactly the scientific project generated during processing.

No additional scientific calculations are performed in this stage.

---

## 25. Export to the Physical Table

The Physical Table receives engineering products already processed by the Offline Pipeline.

Typical inputs include:

- Pin heights
- Projection BMP
- Actuator sequence
- Grid dimensions
- Rotation information

The Physical Table executes only mechanical positioning and synchronized visualization.

---

## 26. Offline Product Repository

A typical project generates the following directory structure.

```text
offline/

├── input/
│   ├── terrain/
│   ├── buildings/
│   ├── imagery/
│   └── metadata/
│
├── products/
│   ├── scientific/
│   ├── final/
│   ├── csv/
│   ├── bmp/
│   ├── json/
│   └── snapshots/
│
└── logs/
```

This organization separates raw data from generated engineering products.

---

## 27. Scientific Logging

Every Offline execution generates execution logs.

Typical information includes:

- Start time
- End time
- Processing duration
- Loaded datasets
- CRS conversion
- Rotation angle
- Grid dimensions
- Exported products
- Validation status
- Warnings
- Errors

Logs support debugging, reproducibility and scientific auditing.

---

## 28. Error Handling

Typical processing errors include:

- Missing datasets
- Invalid CRS
- Corrupted raster
- Missing building data
- Grid generation failure
- Metadata inconsistency
- Export failure

Whenever an error occurs, processing shall stop before generating operational products.

---

## 29. Performance Considerations

The Offline Pipeline prioritizes scientific correctness over execution speed.

Performance optimizations include:

- Raster caching
- Parallel processing
- NumPy vectorization
- Spatial indexing
- Incremental processing

Scientific accuracy shall never be sacrificed for execution speed.

---

## 30. Engineering Configuration

The Offline Pipeline is fully configurable.

Typical configuration parameters include:

- Project Latitude
- Project Longitude
- Project Centroid
- Project Rotation Angle
- Grid Rows
- Grid Columns
- Cell Size
- Maximum Pin Height
- Height Normalization Method
- Output CRS
- Export Directory

These parameters define a complete engineering project.

---

## 31. Scientific Workflow Example

A typical processing sequence is illustrated below.

```text
User selects location

↓

User explores the globe

↓

User rotates the project

↓

User confirms project orientation

↓

System computes centroid

↓

System generates bounding box

↓

System creates scientific grid

↓

System samples terrain

↓

System samples buildings

↓

System computes total height

↓

System generates rasters

↓

System exports BMP

↓

System exports CSV

↓

System generates metadata

↓

System validates outputs

↓

Project ready for IPT-CitySpace
```

The workflow is identical for every processed project.

---

## 32. Engineering Contracts

The Offline Pipeline generates products compliant with the engineering contracts adopted by Globe-CitySpace.

Examples include:

- Physical Table Contract
- Zigzag Contract
- Pin Layout Contract
- Spatial Layout Contract
- Metadata Contract

These contracts guarantee interoperability between all software modules.

---

## 33. Offline Explorer Responsibilities

The Explorer interface is responsible for:

- Geographic navigation
- Dataset visualization
- Area selection
- Project rotation
- Grid preview
- Scientific parameter definition

The Explorer does not perform real-time table control.

Its responsibility ends after validated scientific products are generated.

---

## 34. Rotation Requirement

The Project Rotation Angle is considered an engineering requirement.

Once the operator confirms the orientation during the exploration phase:

- the rotated grid becomes the official project grid;
- the rotated image becomes the official projection image;
- the rotated coordinate frame becomes the engineering reference frame.

Geographic North remains preserved internally but is no longer required to coincide with the table Y-axis.

This requirement allows projects to be naturally aligned with roads, railways, rivers, industrial plants or any dominant geographic feature.

---

## 35. Offline Deliverables

At the end of processing, the Offline Pipeline delivers a complete engineering package.

The package includes:

- Scientific rasters
- BMP projections
- CSV datasets
- NumPy matrices
- Metadata
- Validation reports
- Actuator plans

This package is the only input required by the operational environment.

---

## 36. Offline Pipeline Benefits

The adopted Offline architecture provides several engineering advantages.

These include:

- Scientific reproducibility
- Modular processing
- Deterministic outputs
- Complete traceability
- Independent visualization
- Hardware independence
- Reusable scientific products

The same project can therefore be visualized multiple times without repeating scientific processing.

---

## 37. Future Evolution

The Offline Pipeline was designed to support future capabilities without changing its core architecture.

Examples include:

- Automatic data acquisition
- Cloud processing
- Drone photogrammetry
- LiDAR ingestion
- Artificial Intelligence
- Automatic building extraction
- Automatic road alignment
- Multi-resolution processing
- Global Digital Twin generation

The modular architecture allows these features to be incorporated incrementally.

---

## 38. Recommended Scientific Repository

Scientific products generated by the Offline Pipeline should be stored separately from the source code.

Recommended structure:

```text
Scientific_Data/

├── Projects/
│
├── DSM/
│
├── DTM/
│
├── Buildings/
│
├── Orthophotos/
│
├── Scientific_Products/
│
├── Metadata/
│
├── Reports/
│
└── Snapshots/
```

This organization simplifies backup, sharing and long-term preservation.

---

## 39. Chapter Summary

The Offline Scientific Pipeline is responsible for transforming geographic information into reproducible engineering products.

Its responsibilities include:

- geographic exploration;
- project definition;
- project rotation;
- scientific sampling;
- terrain processing;
- building processing;
- raster generation;
- metadata generation;
- validation;
- export.

The introduction of the **Project Rotation Angle** establishes a local engineering reference frame that is preserved throughout the complete scientific workflow.

Once accepted during the exploration phase, the project orientation becomes immutable and is applied consistently to every scientific product generated by Globe-CitySpace.

---

# Next Chapter

**Chapter 07 — Globe-CitySpace**

---

===========================================================

END OF DOCUMENT

===========================================================