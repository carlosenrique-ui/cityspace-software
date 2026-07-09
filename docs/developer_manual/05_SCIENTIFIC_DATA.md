# Globe-CitySpace Engineering Handbook

---

# Chapter 05 — Scientific Data

## 1. Purpose

This chapter describes the scientific datasets used by Globe-CitySpace and IPT-CitySpace. It defines how terrain, buildings, grids, coordinate systems, raster products and metadata are generated to ensure scientific reproducibility.

The scientific pipeline is deterministic. Given the same input parameters, the system must always generate identical outputs.

---

## 2. Scientific Principles

The scientific model follows these principles:

- Reproducibility
- Deterministic processing
- Coordinate preservation
- Metric accuracy
- Complete metadata generation
- Open scientific formats
- Versioned datasets

Every generated product must be traceable back to its original input datasets.

---

## 3. Scientific Coordinate Systems

The project uses multiple coordinate systems simultaneously.

### Geographic Coordinates

- Latitude
- Longitude
- WGS84 (EPSG:4326)

Used for:

- Global navigation
- Cesium
- Globe visualization

---

### Projected Coordinates

Whenever metric calculations are required, data are transformed into the appropriate UTM zone.

Used for:

- Grid generation
- Area calculation
- Distance calculation
- Cell dimensions
- Scientific exports

All metric computations are performed in projected coordinates.

---

## 4. Scientific Inputs

Typical scientific inputs include:

- Digital Terrain Models (DTM)
- Digital Surface Models (DSM)
- Orthophotos
- Satellite imagery
- Building footprints
- Building heights
- Vector layers
- Raster layers

The processing pipeline is independent of the original data provider.

---

## 5. Scientific Outputs

The scientific pipeline generates standardized outputs that can be consumed by every subsystem.

Typical products include:

- Terrain raster
- Building raster
- Combined height raster
- Projection BMP
- Height BMP
- Grid CSV
- Scientific metadata
- Grid NumPy arrays
- Actuator plans
- Visualization products

Each output is deterministic and reproducible.

---

## 6. Terrain Model

Terrain elevation is represented by the Digital Terrain Model (DTM).

The DTM contains only the bare earth surface.

It excludes:

- Buildings
- Trees
- Vehicles
- Temporary objects

Typical global sources include:

- FABDEM
- Copernicus DEM
- SRTM

Higher-resolution municipal DTMs may replace global datasets whenever available.

---

## 7. Surface Model

The Digital Surface Model (DSM) represents the visible surface.

It includes:

- Terrain
- Buildings
- Vegetation
- Infrastructure

DSM data may originate from:

- LiDAR
- Drone photogrammetry
- Airborne photogrammetry
- Satellite stereo imagery

---

## 8. Building Model

Buildings may be obtained from several sources.

Examples:

- Municipal GIS
- OpenStreetMap
- Overture Maps
- Global Building Atlas
- Microsoft Building Footprints

Building geometry and height are treated independently.

Whenever only footprints are available, building height estimation may be applied according to the scientific configuration.

---

## 9. Scientific Height Model

The scientific height model separates terrain elevation from building elevation.

Definitions:

Terrain Height

```
Zterrain
```

Building Height

```
Zbuilding
```

Total Height

```
Ztotal = Zterrain + Zbuilding
```

This separation preserves scientific traceability and allows different visualization strategies.

---

## 10. Scientific Rotation Model

A project rotation may be defined during the exploration phase.

This rotation aligns the study area with its dominant orientation (for example, a straight road, an airport runway or an urban corridor).

The selected angle becomes part of the scientific metadata and shall be preserved throughout the complete processing pipeline.

Definitions:

```
Project Rotation Angle
```

```
Rotation Center = Project Centroid
```

The rotation is always applied around the project centroid.

This parameter affects:

- Scientific grid
- Projection raster
- Height raster
- Grid coordinates
- BMP products
- CSV products
- Virtual table
- Physical table
- Metadata

The original geographic coordinates remain unchanged.

Only the local project reference frame is rotated.

---

## 11. Grid Reference System

Every project generates a scientific grid.

Each grid cell contains:

- Row
- Column
- Latitude
- Longitude
- UTM coordinates
- Terrain height
- Building height
- Total height
- Gray level
- Pin height

Each cell represents a deterministic spatial sample.

---

## 12. Scientific Metadata

Every generated project includes metadata describing:

- Input datasets
- CRS
- Processing date
- Processing software
- Software version
- Rotation angle
- Grid dimensions
- Cell size
- Number of rows
- Number of columns
- Bounding box
- Project centroid

The metadata guarantees complete reproducibility.

---

## 13. Raster Products

Typical raster products include:

Projection BMP

Represents the projected visualization used by IPT-CitySpace.

Height BMP

Represents normalized height values.

Terrain Raster

Contains terrain elevation only.

Building Raster

Contains building height only.

Combined Raster

Represents

```
Terrain + Buildings
```

Each raster preserves the scientific reference system defined for the project.

---

## 14. Scientific CSV Products

CSV products provide structured information for analysis.

Examples:

- Grid metrics
- Cell coordinates
- Terrain heights
- Building heights
- Total heights
- Pin heights
- Actuator sequence

CSV files are intended for validation, reproducibility and interoperability.

---

## 15. Scientific BMP Products

BMP products are optimized for high-speed visualization and projection mapping.

The most common products are:

- Projection BMP
- Height BMP
- Grayscale BMP
- Binary Mask BMP

Each BMP is generated directly from the scientific raster while preserving the project orientation.

No visual manipulation shall modify the scientific values represented by each pixel.

---

## 16. Scientific NumPy Products

NumPy arrays are generated to accelerate scientific processing.

Typical arrays include:

- Terrain matrix
- Building matrix
- Total height matrix
- Gray level matrix
- Pin height matrix

These matrices are consumed by simulation modules, optimization algorithms and visualization components.

---

## 17. Scientific Validation

Every generated project shall pass a validation stage.

Validation verifies:

- Coordinate consistency
- CRS consistency
- Grid dimensions
- Cell dimensions
- Height normalization
- Raster dimensions
- Metadata completeness
- Rotation angle consistency

Projects failing validation shall not be exported to the physical table.

---

## 18. Scientific Reproducibility

The Globe-CitySpace scientific pipeline is deterministic.

Given:

- identical datasets;
- identical software version;
- identical project centroid;
- identical project rotation angle;
- identical grid dimensions;
- identical configuration parameters;

the generated outputs must be identical.

This guarantees scientific reproducibility across different workstations and institutions.

---

## 19. North Orientation

The geographic North is always preserved in the project metadata.

However, the project reference frame may be rotated according to the Project Rotation Angle defined during the exploration phase.

Consequently:

- the scientific grid is rotated;
- the projected image is rotated;
- the virtual table is rotated;
- the physical table uses the rotated reference frame.

The 2D interface shall display a North Arrow indicating the current angular offset between Geographic North and the project Y-axis.

The 3D visualization shall not display a fixed "North" label on the Y-axis, since the local project frame may be intentionally rotated.

This approach preserves both scientific accuracy and user interpretation.

---

## 20. Scientific Versioning

All scientific products shall be version controlled.

Version information includes:

- Software version
- Processing version
- Dataset version
- Metadata version
- Export version

Scientific versioning guarantees traceability throughout the complete project lifecycle.

---

## 21. Scientific Data Providers

The architecture is data-provider independent.

Typical providers include:

Global datasets

- FABDEM
- Copernicus DEM
- SRTM
- Overture Maps
- Global Building Atlas

Municipal datasets

- LiDAR
- DSM
- DTM
- Orthophotos
- Cadastral buildings

Commercial datasets

- WorldDEM
- WorldDEM Neo
- Google Photorealistic 3D Tiles
- Cesium Terrain

The processing pipeline remains identical regardless of the source.

---

## 22. Scientific Quality Levels

Datasets are classified according to spatial quality.

Level 1

Global products

Typical resolution:

30 m

Applications:

- Continental
- National
- Regional

---

Level 2

Municipal products

Typical resolution:

0.5–5 m

Applications:

- Urban planning
- Infrastructure
- Environmental analysis

---

Level 3

Engineering products

Typical resolution:

5–50 cm

Applications:

- Digital Twins
- Tangible Tables
- Engineering Simulation
- Precision Mapping

---

## 23. Scientific Processing Sequence

The scientific workflow follows the sequence below.

1. Load input datasets

2. Validate CRS

3. Transform to projected coordinates

4. Compute project centroid

5. Apply Project Rotation Angle

6. Generate scientific grid

7. Sample terrain

8. Sample buildings

9. Compute total height

10. Normalize values

11. Generate rasters

12. Generate BMP products

13. Generate CSV products

14. Generate metadata

15. Validate outputs

16. Export products

Every execution follows exactly the same sequence.

---

## 24. Engineering Requirements

The scientific subsystem shall:

- preserve metric accuracy;
- preserve coordinate consistency;
- preserve project rotation;
- preserve reproducibility;
- generate deterministic outputs;
- support multiple data providers;
- support multiple resolutions;
- support future scientific datasets.

These requirements ensure long-term maintainability of Globe-CitySpace.

---

## 25. Scientific Directory Organization

Scientific datasets should be maintained outside the software repository.

The recommended organization is:

```text
Scientific_Data/

├── DSM/
├── DTM/
├── Orthophotos/
├── Buildings/
├── Height_Maps/
├── Projection_Maps/
├── CSV/
├── BMP/
├── Metadata/
├── Snapshots/
└── Reports/
```

The GitHub repository stores only the software required to generate these products.

The scientific repository stores the generated datasets.

---

## 26. Scientific Metadata Example

Each project should generate metadata similar to the following.

```json
{
    "project_name": "IPT-CitySpace",
    "crs": "EPSG:31983",
    "latitude": -23.5567944,
    "longitude": -46.7373288,
    "rotation_deg": -26.02,
    "rotation_direction": "clockwise",
    "rotation_pivot": "project_centroid",
    "north_relative_to_table_y_deg": -26.02,
    "grid_rows": 8,
    "grid_columns": 16,
    "cell_size_cm": 2,
    "processing_version": "2.0"
}
```

These metadata describe the scientific reference frame used by the entire project.

---

## 27. Scientific Data Lifecycle

The complete scientific data lifecycle is summarized below.

```text
Raw Geographic Data

↓

Coordinate Validation

↓

Coordinate Transformation

↓

Project Centroid

↓

Project Rotation

↓

Scientific Grid

↓

Terrain Sampling

↓

Building Sampling

↓

Scientific Products

↓

Validation

↓

Metadata

↓

Export

↓

Virtual Table

↓

Physical Table
```

Every stage preserves the scientific integrity of the project.

---

## 28. Chapter Summary

The Scientific Data subsystem is the foundation of Globe-CitySpace.

It guarantees that all geographic information is transformed into reproducible engineering products while preserving metric accuracy, coordinate consistency and complete traceability.

The introduction of the **Project Rotation Angle** allows each project to define its own local engineering reference frame.

Once defined during the exploration phase, this angle becomes part of the scientific metadata and shall be applied consistently to:

- scientific grid;
- raster products;
- BMP products;
- CSV products;
- projection mapping;
- virtual table;
- physical table.

The Geographic North remains preserved in the metadata, while the project reference frame becomes the operational reference used throughout the engineering workflow.

---

# Next Chapter

**Chapter 06 — Offline Scientific Pipeline**

---

===========================================================

END OF DOCUMENT

===========================================================