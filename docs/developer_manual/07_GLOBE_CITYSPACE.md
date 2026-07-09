# Globe-CitySpace

---

## 1. Purpose

Globe-CitySpace is the global geographic exploration component of the IPT-CitySpace ecosystem.

Its purpose is to allow an engineer or researcher to navigate anywhere on Earth, define a study area, align the project with the local urban geometry and generate all scientific inputs required by the Offline Pipeline.

Unlike a conventional GIS viewer, Globe-CitySpace is the engineering front-end responsible for defining the spatial reference that will be preserved throughout the complete processing chain.

---

## 2. Main Responsibilities

Globe-CitySpace performs the following tasks:

- global geographic navigation;
- latitude and longitude selection;
- project positioning;
- project orientation;
- project rotation;
- grid alignment;
- area definition;
- scientific validation;
- project export.

The resulting project becomes the input for the complete scientific workflow.

---

## 3. Geographic Navigation

The application allows continuous navigation over the Earth's surface.

Supported operations include:

- zoom;
- pan;
- orbit;
- camera tilt;
- north orientation;
- free exploration.

Navigation is independent of the scientific processing stage.

---

## 4. Study Area Definition

After locating the desired region, the user defines the project area.

The selected region becomes the project boundary that will be processed by the Offline Pipeline.

Typical study areas include:

- university campuses;
- industrial facilities;
- city blocks;
- neighborhoods;
- municipalities;
- metropolitan regions.

The project boundary remains associated with the project metadata.

---

## 5. Project Center

Every project has a single reference point.

This point corresponds to the project centroid.

The centroid is used for:

- project identification;
- metadata generation;
- coordinate transformations;
- grid generation;
- visualization synchronization.

All exported products reference this same geographic position.

---

## 6. Grid Generation

Once the project area is defined, Globe-CitySpace generates the engineering grid.

The grid represents the future actuator matrix used by IPT-CitySpace.

Grid parameters include:

- number of rows;
- number of columns;
- physical dimensions;
- spatial resolution;
- geographic extent.

Each grid cell corresponds to one future actuator.

---

## 7. Project Orientation

One of the most important engineering decisions occurs during the exploration phase.

The user chooses the preferred orientation of the project.

This orientation is generally selected so that the dominant urban geometry becomes visually aligned.

Examples include:

- streets;
- avenues;
- building facades;
- industrial corridors;
- airport runways.

This orientation improves interpretation during later visualization.

---

## 8. Rotation Management

Unlike traditional GIS applications, Globe-CitySpace treats rotation as a permanent engineering parameter.

The selected rotation angle becomes part of the project metadata.

Typical examples include:

- road alignment;
- river alignment;
- railway alignment;
- runway alignment;
- building alignment.

The rotation is preserved throughout the complete workflow.

---

## 9. Engineering Rotation Angle

The project stores a rotation angle measured relative to geographic north.

Example:

Rotation = -26.02°

This means that the project has been rotated 26.02 degrees clockwise relative to true north.

The stored value is later reused by all subsequent modules.

---

## 10. Grid Rotation

The engineering grid is rotated together with the project.

The grid is never rotated independently.

Instead, both:

- raster;
- grid;
- project boundary;
- metadata;

share exactly the same rotation.

This guarantees that every actuator corresponds to the same geographic location regardless of visualization.

---

## 11. North Arrow

Because the project itself may be rotated, geographic north no longer coincides with the vertical axis of the engineering view.

For this reason:

- the North Arrow is rotated according to the stored project angle;
- the arrow always indicates true geographic north;
- the engineering grid remains aligned with the selected project orientation.

This behavior allows the operator to immediately understand both the engineering orientation and the geographic orientation.

---

## 12. Design Decision

A design decision adopted in IPT-CitySpace is that the 2D scientific visualization contains the rotated North Arrow instead of forcing the project to remain north-up.

Advantages include:

- better visualization of urban geometry;
- easier interpretation of streets;
- improved actuator alignment;
- simpler comparison with engineering drawings;
- preservation of geographic reference.

---

## 13. 3D Visualization

The 3D globe remains geographically correct.

The world itself is never rotated.

Instead:

- the project grid rotates;
- the project boundary rotates;
- the camera may rotate;
- the Earth remains fixed.

To avoid ambiguity, the fixed "North" text shown along the Y axis is removed from the engineering visualization.

The North Arrow shown in the 2D scientific view becomes the official geographic reference.

---

## 14. Project Metadata

Every exported project contains orientation metadata.

Typical metadata include:

- centroid latitude;
- centroid longitude;
- rotation angle;
- geographic extent;
- grid dimensions;
- spatial resolution;
- CRS;
- export date.

This information guarantees complete reproducibility of the project.

---

## 15. Scientific Export

After validation, Globe-CitySpace exports all scientific inputs required by the Offline Pipeline.

Typical exported products include:

- project metadata;
- scientific raster;
- height raster;
- building raster;
- terrain raster;
- engineering grid;
- actuator grid;
- geographic boundary.

These products constitute the official scientific dataset for the project.

---

## 16. Supported Coordinate Systems

Although Globe-CitySpace operates globally, all exported products preserve their spatial reference.

Supported coordinate systems include:

- WGS84 Geographic Coordinates;
- projected coordinate systems;
- UTM zones;
- local engineering systems.

The selected CRS is recorded in the project metadata.

---

## 17. Integration with the Offline Pipeline

Globe-CitySpace is the first stage of the complete engineering workflow.

Its outputs become the direct inputs to the Offline Pipeline.

The processing sequence is:

1. Geographic exploration.
2. Project definition.
3. Rotation selection.
4. Grid generation.
5. Scientific export.
6. Offline scientific processing.

This separation keeps visualization independent from scientific computation.

---

## 18. Reproducibility

One important design objective is reproducibility.

Any engineer should be able to recreate exactly the same project by using:

- centroid;
- geographic extent;
- CRS;
- rotation angle;
- grid dimensions.

No manual adjustments should be necessary after the project has been exported.

---

## 19. Drone Mapping Support

The selected project orientation is also applicable to aerial surveys.

For example, during drone photogrammetry acquisition, the engineering team may intentionally align the flight mission with the dominant urban geometry.

The resulting orthomosaic can therefore be imported directly into Globe-CitySpace while preserving the same project orientation.

This minimizes unnecessary rotations during later processing stages and simplifies comparison between satellite imagery, drone imagery and engineering grids.

---

## 20. Chapter Summary

This chapter presented the Globe-CitySpace exploration environment.

Its responsibilities include:

- global navigation;
- project definition;
- centroid selection;
- engineering rotation;
- grid generation;
- metadata generation;
- scientific export.

The stored project orientation becomes a permanent engineering parameter that is propagated throughout the complete IPT-CitySpace workflow, ensuring consistency between the globe visualization, the Offline Pipeline, the Virtual Table and the Physical Table.

---

# Next Chapter

**Chapter 08 — IPT-CitySpace**

---

===========================================================

END OF DOCUMENT

===========================================================