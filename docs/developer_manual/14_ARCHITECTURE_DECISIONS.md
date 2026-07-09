# Globe-CitySpace Engineering Handbook

# Chapter 14 — Architecture Decisions

---

## 1. Purpose

This chapter documents the principal engineering decisions adopted during the development of Globe-CitySpace.

Its objectives are to:

- explain architectural choices;
- preserve engineering knowledge;
- avoid repeating previous discussions;
- assist future developers;
- document the rationale behind important design decisions.

These decisions should only be modified after careful technical evaluation.

---

## 2. Why Architecture Decisions Matter

Software architecture evolves over many years.

Future developers frequently understand **what** the software does, but not **why** specific engineering choices were made.

Recording architecture decisions helps preserve:

- engineering consistency;
- scientific reproducibility;
- maintainability;
- long-term sustainability.

This document serves as the historical memory of the project.

---

## 3. Decision 001 — Separation Between Globe-CitySpace and IPT-CitySpace

### Decision

The project is divided into two independent applications:

- Globe-CitySpace;
- IPT-CitySpace.

### Motivation

The Globe is responsible for exploration and scientific preparation.

IPT-CitySpace is responsible for engineering visualization and interaction with the tangible table.

Separating responsibilities simplifies maintenance and allows independent evolution of both systems.

### Consequences

Advantages include:

- modular architecture;
- independent testing;
- easier maintenance;
- cleaner source code;
- better scalability.

---

## 4. Decision 002 — Offline Before Online

### Decision

All scientific processing is executed before real-time operation.

### Motivation

Scientific calculations may require considerable computational resources.

Executing them offline guarantees deterministic and reproducible outputs.

Only validated products are transferred to the online environment.

---

## 5. Decision 003 — Scientific Processing is Deterministic

### Decision

The scientific pipeline must always produce identical outputs when executed with identical inputs.

### Motivation

Engineering reproducibility is one of the fundamental principles of the project.

Scientific datasets, metadata and processing parameters are preserved to guarantee identical results across different executions.

---

## 6. Decision 004 — Height Model = Terrain + Building

### Decision

The engineering height model adopted by Globe-CitySpace is:

```
Total Height

=

Terrain Height

+

Building Height
```

### Motivation

Separating terrain and building components preserves scientific clarity while allowing each component to be independently validated.

The combined model represents the surface reproduced by the tangible table.

### Consequences

Benefits include:

- reproducible height computation;
- independent validation;
- modular processing;
- improved scientific transparency.

---

## 7. Decision 005 — Engineering Grid Based on Centroids

### Decision

All spatial sampling is performed using the centroid of each engineering grid cell.

### Motivation

Centroid sampling guarantees a deterministic and geometrically consistent representation of the study area.

Alternative approaches based on cell corners or random sampling were intentionally rejected.

### Consequences

This decision provides:

- consistent raster extraction;
- reproducible spatial analysis;
- simplified coordinate transformations.

---

## 8. Decision 006 — Grid Rotation During Exploration

### Decision

The engineering grid may be rotated during the exploration phase before scientific processing begins.

### Motivation

Many study areas are naturally aligned with roads, buildings or engineering corridors rather than geographic north.

Allowing rotation improves:

- raster utilization;
- engineering interpretation;
- tangible table presentation.

The selected rotation angle becomes part of the project metadata.

---

## 9. Decision 007 — Preserve the Project Rotation Angle

### Decision

Once defined, the Project Rotation Angle is preserved throughout the entire workflow.

### Motivation

Changing the orientation during later stages would compromise reproducibility.

The same angle is reused by:

- Offline Pipeline;
- IPT-CitySpace;
- Projection Mapping;
- Virtual Table;
- Physical Table.

This guarantees geometric consistency.

---

## 10. Decision 008 — North Arrow Represents Geographic North

### Decision

The north arrow displayed in IPT-CitySpace represents geographic north relative to the rotated engineering project.

### Motivation

After grid rotation, the engineering Y-axis is no longer necessarily aligned with geographic north.

Displaying the stored Project Rotation Angle avoids ambiguity while preserving the geographic reference.

---

## 11. Decision 009 — Globe-CitySpace Does Not Control Hardware

### Decision

Globe-CitySpace is exclusively responsible for geographic exploration and scientific data preparation.

Hardware control is delegated to IPT-CitySpace.

### Motivation

Separating hardware control from geographic exploration simplifies software architecture and improves maintainability.

It also allows the exploration component to evolve independently of the tangible table.

### Consequences

Benefits include:

- lower software coupling;
- improved modularity;
- easier testing;
- independent software deployment.

---

## 12. Decision 010 — Scientific Metadata is Mandatory

### Decision

Every engineering product generated by the Offline Pipeline must include complete scientific metadata.

### Motivation

Metadata preserves reproducibility and documents the processing conditions used to generate each output.

Typical metadata includes:

- CRS;
- Bounding Box;
- Grid dimensions;
- Raster resolution;
- Processing date;
- Data sources;
- Project Rotation Angle.

### Consequences

Scientific products remain reproducible even after many years.

---

## 13. Decision 011 — Explorer is Independent of Data Sources

### Decision

The Globe-CitySpace Explorer should operate independently of any specific data provider.

### Motivation

Geospatial datasets evolve over time.

By isolating data acquisition from visualization, the platform can incorporate new sources without major architectural changes.

Examples include:

- FABDEM;
- Copernicus DEM;
- OpenTopography;
- Municipal DTM repositories;
- Future datasets.

### Consequences

The platform remains flexible and extensible.

---

## 14. Decision 012 — Scientific Contracts Define Interfaces

### Decision

Communication between software modules is governed by engineering contracts.

### Motivation

Engineering contracts eliminate ambiguity regarding:

- file formats;
- coordinate systems;
- actuator mapping;
- metadata structures;
- grid dimensions.

### Consequences

Different software components can evolve independently while maintaining compatibility.

---

## 15. Decision 013 — Virtual Table Before Physical Table

### Decision

Every engineering workflow should first be validated using the Virtual Table.

### Motivation

Testing in software is faster, safer and less expensive than testing directly on hardware.

Only validated engineering products are transferred to the Physical Table.

### Consequences

This decision reduces hardware risks and accelerates software development.

---

## 16. Decision 014 — Projection Mapping Uses Preprocessed Products

### Decision

Projection Mapping is performed exclusively using products generated by the Offline Scientific Pipeline.

### Motivation

Real-time raster processing would unnecessarily increase computational complexity and reduce system responsiveness.

By using preprocessed products, the projection system remains lightweight and deterministic.

### Consequences

Benefits include:

- faster demonstrations;
- deterministic visualization;
- simplified synchronization;
- improved reliability.

---

## 17. Decision 015 — Scientific Scale is Preserved

### Decision

The engineering scale selected for the project remains fixed throughout the processing workflow.

### Motivation

Changing the engineering scale after raster generation would invalidate grid dimensions, actuator mapping and projection geometry.

The selected scale therefore becomes part of the project metadata.

### Consequences

Engineering consistency is preserved across all generated products.

---

## 18. Decision 016 — One Grid Cell Corresponds to One Actuator

### Decision

Each engineering grid cell corresponds to exactly one actuator in the Physical Table.

### Motivation

A one-to-one mapping simplifies:

- synchronization;
- debugging;
- engineering calculations;
- maintenance.

No interpolation between actuators is performed during normal operation.

### Consequences

The relationship between software and hardware remains deterministic.

---

## 19. Decision 017 — Geographic Data Remains Unmodified

### Decision

Original scientific datasets are never modified during processing.

Derived engineering products are generated as independent outputs.

### Motivation

Preserving original datasets allows future reprocessing using improved algorithms without losing the source information.

### Consequences

Scientific integrity and reproducibility are maintained.

---

## 20. Decision 018 — Modular Software Architecture

### Decision

Globe-CitySpace follows a modular architecture composed of independent software components.

Examples include:

- Explorer;
- Offline Pipeline;
- IPT-CitySpace;
- Virtual Table;
- Physical Table.

### Motivation

Modules communicate through well-defined interfaces rather than direct dependencies.

### Consequences

The platform becomes easier to maintain, test and extend.

---

## 21. Decision 019 — Open Standards Whenever Possible

### Decision

Whenever technically feasible, Globe-CitySpace adopts open standards and open geospatial formats.

Examples include:

- GeoTIFF;
- GeoJSON;
- CSV;
- PNG;
- BMP;
- WGS84;
- UTM.

### Motivation

Open standards improve interoperability and reduce long-term technological dependency.

### Consequences

Engineering products remain compatible with a wide range of scientific and GIS software.

---

## 22. Decision 020 — Platform Independence

### Decision

The software architecture should remain as independent as possible from operating systems and hardware platforms.

### Motivation

The platform should be executable in different environments, including:

- Windows;
- Linux;
- WSL;
- Docker;
- future cloud deployments.

### Consequences

Migration and deployment become significantly easier.

---

## 23. Decision 021 — Documentation Evolves with the Software

### Decision

Engineering documentation is considered an integral component of the software project.

Documentation must evolve together with the implementation.

### Motivation

Outdated documentation quickly loses value.

Maintaining synchronized documentation reduces onboarding time and improves maintainability.

### Consequences

Every significant architectural modification should be reflected in the Engineering Handbook.

---

## 24. Decision 022 — Scientific Validation Before Demonstration

### Decision

Every engineering product should be scientifically validated before public demonstration.

### Motivation

Validation activities include:

- geometric verification;
- elevation consistency;
- metadata inspection;
- visual analysis;
- reproducibility checks.

### Consequences

Only validated engineering products are presented during demonstrations and technical evaluations.

---

## 25. Decision 023 — Long-Term Maintainability

### Decision

Long-term maintainability is considered a primary architectural objective.

### Motivation

The project is expected to evolve over many years and potentially involve multiple developers and institutions.

Architectural decisions therefore prioritize:

- readability;
- modularity;
- documentation;
- reproducibility;
- extensibility.

### Consequences

Future developers can understand and extend the platform with reduced learning effort.

---

## 26. Decision 024 — Engineering Knowledge Must Be Preserved

### Decision

Engineering knowledge shall be preserved through documentation rather than relying solely on individual experience.

### Motivation

Software projects frequently outlive their original developers.

Maintaining comprehensive documentation ensures that architectural knowledge remains available for future engineers, researchers and institutions.

### Consequences

The Engineering Handbook becomes part of the software architecture itself and shall be maintained together with the source code.

---

## 27. Architecture Review Process

Architecture decisions are expected to evolve over time.

However, modifications should only occur after:

- technical evaluation;
- scientific validation;
- engineering discussion;
- documentation update.

Every significant architectural change should be recorded in this chapter.

---

## 28. Architecture Decision Record (ADR) Philosophy

This chapter follows the principles of an Architecture Decision Record (ADR).

Each recorded decision includes:

- the decision itself;
- its motivation;
- expected consequences.

This structure preserves the engineering rationale behind the software architecture.

---

## 29. Chapter Summary

This chapter documents the principal engineering decisions that define the Globe-CitySpace architecture.

These decisions establish:

- software modularity;
- deterministic scientific processing;
- engineering reproducibility;
- separation of responsibilities;
- long-term maintainability.

Future architectural modifications should extend these principles rather than replace them without strong technical justification.

---

# Next Chapter

**Chapter 15 — Troubleshooting**

---

===========================================================

END OF DOCUMENT

===========================================================

