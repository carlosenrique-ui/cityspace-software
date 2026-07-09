# Globe-CitySpace Engineering Handbook

---

# Chapter 04

# Directory Structure

**Version:** 2.0

**Project:** Globe-CitySpace

**Institution:** Institute for Technological Research (IPT)

São Paulo, Brazil

---

# 1. Purpose

This chapter documents the directory organization adopted by the Globe-CitySpace platform.

The objective is to make the repository self-explanatory, allowing future developers to quickly understand where each component is located.

A standardized directory structure is fundamental for software maintenance, scalability and collaborative development.

---

# 2. General Organization

The repository is organized into major engineering modules.

Each module has a well-defined responsibility and should avoid depending unnecessarily on the internal implementation of the others.

At the highest level the repository is organized approximately as follows:

```text
README.md

Dockerfile

docker-compose.yml

offline/

online/

runner/

config/

docs/

globe_cityspace_open/

tests/

scripts/
```

---

# 3. Repository Philosophy

The repository stores software.

Scientific products generated during execution are not part of the source code repository.

Only artifacts required to build, execute and maintain the software should remain under version control.

This approach keeps Git lightweight and simplifies collaboration.

---

# 4. Root Directory

The project root contains:

- project documentation;
- Docker configuration;
- startup scripts;
- engineering documentation;
- scientific software;
- configuration files.

The root directory should remain as clean as possible.

---

# 5. README.md

README.md is the repository entry point.

It explains:

- project objectives;
- main architecture;
- technologies;
- execution;
- documentation;
- developer manual.

Every developer should read the README before exploring the remaining documentation.

---

# 6. Docker Files

Docker configuration is maintained at the repository root.

Typical files include:

```text
Dockerfile

docker-compose.yml

requirements-docker.txt
```

These files define the execution environment.

---

# 7. Startup Scripts

Repository startup scripts automate common development tasks.

Typical examples:

```text
start_demo.sh

start_demo2.sh

run_globe_cityspace_integrated.sh

run_globe_cityspace_integrated_total.sh
```

Developers should prefer these scripts over manual execution whenever possible.

---

# 8. Documentation

All engineering documentation is concentrated inside:

```text
docs/
```

This directory contains architecture documents, technical reports, engineering handbook and supporting documentation.

---

# 9. Engineering Handbook

The developer manual is maintained inside:

```text
docs/

└── developer_manual/
```

This handbook is considered the official technical documentation of the platform.

---

# 10. Chapter Summary

This chapter introduces the overall repository organization.

The following sections describe each major directory individually.

---

**BLOCO 1 DE 6**

# 11. offline/

The **offline/** directory contains the complete scientific processing pipeline.

Its primary responsibility is transforming raw geographic information into scientific products that can later be consumed by the tangible table.

Typical processing performed here includes:

- raster loading;
- vector loading;
- scientific grid generation;
- terrain analysis;
- building analysis;
- height normalization;
- BMP generation;
- CSV generation.

---

# 12. Offline Internal Organization

The Offline module is divided into specialized components.

Typical structure:

```text
offline/

├── adapters/
├── analysis/
├── assets/
├── config/
├── debug/
├── ingestion/
├── loading/
├── pipeline/
├── processing/
├── raster/
├── validation/
├── vector/
├── tests/
```

Each directory performs a specific responsibility within the scientific pipeline.

---

# 13. online/

The **online/** directory contains the execution environment responsible for operating the virtual and physical tangible tables.

Unlike the Offline pipeline, the Online module operates in real time.

Responsibilities include:

- visualization;
- actuator control;
- user interface;
- runtime synchronization;
- projection mapping.

---

# 14. Online Internal Organization

Typical structure:

```text
online/

├── actuators/
├── assets/
├── config/
├── controllers/
├── core/
├── data/
├── hardware/
├── outputs/
├── physical/
├── renderers/
├── runtime/
├── states/
├── tests/
├── ui/
├── visualization/
```

The Online module is intentionally separated from the scientific processing performed by the Offline module.

---

# 15. runner/

The **runner/** directory coordinates software execution.

Its responsibilities include:

- execution flow;
- actuator abstraction;
- runtime orchestration;
- simulation control.

This directory acts as the bridge between Offline processing and Online execution.

---

# 16. config/

The **config/** directory stores project-wide configuration files.

Typical examples include:

- system parameters;
- execution paths;
- engineering constants;
- runtime configuration.

Configuration files should avoid containing executable business logic.

---

# 17. docs/

The **docs/** directory contains all technical documentation.

Typical contents include:

- architecture;
- engineering handbook;
- releases;
- reverse engineering;
- development notes;
- roadmap;
- pipeline documentation.

No source code should be placed inside this directory.

---

# 18. tests/

The **tests/** directory stores automated tests.

Typical categories include:

- unit tests;
- integration tests;
- validation tests;
- regression tests.

Future software modifications should preserve compatibility with existing tests.

---

# 19. scripts/

The **scripts/** directory contains engineering automation scripts.

Typical examples:

- diagnostics;
- validation;
- preprocessing;
- engineering utilities.

Scripts are intended to automate repetitive engineering activities.

---

# 20. Chapter Summary

The first group of directories defines the core engineering organization of Globe-CitySpace.

The remaining sections describe specialized directories responsible for visualization, scientific processing and project integration.

---

**BLOCO 2 DE 6**

# 21. globe_cityspace_open/

The **globe_cityspace_open/** directory contains the global geospatial interface of the platform.

It is responsible for transforming any geographic location into a CitySpace Area that can later be processed by the scientific pipeline.

Main responsibilities include:

- globe visualization;
- city selection;
- latitude/longitude navigation;
- area selection;
- communication with the Offline pipeline.

---

# 22. Globe Internal Organization

Typical organization:

```text
globe_cityspace_open/

├── backend/
├── frontend/
├── core/
├── contracts/
├── data/
├── docs/
├── projects/
```

Each subdirectory has a clearly defined engineering responsibility.

---

# 23. backend/

The **backend/** directory implements the server-side processing of Globe-CitySpace.

Typical responsibilities include:

- request processing;
- scientific orchestration;
- raster loading;
- project creation;
- export generation.

The backend communicates directly with the Offline scientific pipeline.

---

# 24. frontend/

The **frontend/** directory implements the graphical interface presented to the user.

Typical responsibilities include:

- globe visualization;
- CesiumJS integration;
- user interaction;
- area selection;
- project configuration.

The frontend should contain only presentation logic.

---

# 25. core/

The **core/** directory contains reusable software components shared by different Globe-CitySpace modules.

Examples include:

- common algorithms;
- geometry utilities;
- coordinate conversions;
- shared services.

The objective is to reduce code duplication.

---

# 26. contracts/

The **contracts/** directory defines interfaces shared between software modules.

Typical examples include:

- JSON contracts;
- table configuration;
- actuator configuration;
- engineering constants.

Contracts establish stable communication between independent components.

---

# 27. data/

The **data/** directory stores small reference datasets required by the application.

Typical contents include:

- configuration files;
- templates;
- sample data;
- lookup tables.

Large scientific datasets should not be stored here.

---

# 28. projects/

The **projects/** directory stores user-generated project configurations.

Typical information includes:

- Area of Interest (AOI);
- project metadata;
- processing parameters;
- export configuration.

Project definitions should remain lightweight and reproducible.

---

# 29. Separation of Responsibilities

The repository is organized according to functional responsibilities.

```text
Offline

↓

Scientific Processing

↓

Online

↓

Visualization

↓

Runner

↓

Execution Control

↓

Globe

↓

User Interaction
```

Each subsystem should remain independent whenever possible.

---

# 30. Chapter Summary

The Globe-CitySpace repository follows a modular architecture that separates scientific processing, visualization, execution and documentation into independent directories.

This organization improves scalability, simplifies maintenance and facilitates future software evolution.

---

**BLOCO 3 DE 6**

# 31. docs/

The **docs/** directory centralizes the technical documentation of the Globe-CitySpace project.

Its objective is to preserve engineering knowledge independently of the source code.

Typical documentation includes:

- architecture;
- scientific pipeline;
- engineering handbook;
- developer manual;
- release notes;
- reverse engineering reports.

Documentation evolves together with the software.

---

# 32. architecture/

The **architecture/** directory stores high-level architectural documents.

Typical contents include:

- software architecture;
- component diagrams;
- data flow diagrams;
- system integration;
- design decisions.

Architecture documents describe *why* the software is organized as it is.

---

# 33. developer_manual/

The **developer_manual/** directory contains the complete technical handbook for developers.

Its purpose is to accelerate onboarding and preserve institutional knowledge.

Typical chapters include:

- project overview;
- architecture;
- development environment;
- scientific pipeline;
- repository organization;
- execution workflow.

This handbook is intended to remain synchronized with the repository.

---

# 34. development/

The **development/** directory stores documents related to ongoing software evolution.

Typical examples include:

- implementation notes;
- design proposals;
- technical experiments;
- development plans;
- engineering discussions.

This material supports active software development.

---

# 35. reverse_engineering/

The **reverse_engineering/** directory documents analyses performed on legacy components.

Typical contents include:

- recovered workflows;
- software mapping;
- dependency analysis;
- migration studies;
- architectural reconstruction.

These documents support software modernization.

---

# 36. releases/

The **releases/** directory records the evolution of Globe-CitySpace.

Typical contents include:

- release notes;
- version history;
- major milestones;
- deployment information.

Release documentation improves project traceability.

---

# 37. Documentation Philosophy

Documentation is treated as a permanent engineering asset.

Every major architectural decision should eventually be documented.

Documentation is maintained using Markdown to ensure long-term accessibility.

---

# 38. Engineering Knowledge Preservation

The repository aims to preserve engineering knowledge beyond individual developers.

Documentation reduces onboarding time, simplifies maintenance and improves long-term sustainability.

---

# 39. Recommended Documentation Workflow

Recommended sequence:

```text
Architecture

↓

Implementation

↓

Testing

↓

Documentation

↓

Review

↓

Release
```

Maintaining documentation continuously is preferable to documenting only after implementation.

---

# 40. Chapter Summary

The documentation directories organize the technical knowledge of Globe-CitySpace into specialized collections that support development, maintenance and future evolution of the platform.

---

**BLOCO 4 DE 6**

# 41. runner/

The **runner/** directory contains the execution scripts responsible for orchestrating Globe-CitySpace workflows.

Typical responsibilities include:

- launching processing pipelines;
- executing scientific workflows;
- coordinating offline processing;
- invoking visualization modules;
- managing execution sequences.

The runner acts as the operational entry point of the platform.

---

# 42. config/

The **config/** directory centralizes configuration files used throughout the project.

Typical configuration files include:

- environment settings;
- application parameters;
- processing options;
- default paths;
- execution profiles.

Centralizing configuration improves maintainability and reproducibility.

---

# 43. Root-Level Files

Several important files are stored at the repository root.

Examples include:

- README.md
- Dockerfile
- docker-compose.yml
- requirements.txt
- start_demo.sh
- start_demo2.sh

These files provide project entry points and deployment instructions.

---

# 44. Repository Design Principles

The repository follows several engineering principles:

- modular organization;
- separation of concerns;
- reproducibility;
- maintainability;
- scalability;
- documentation-first philosophy.

These principles simplify long-term software evolution.

---

# 45. Long-Term Maintainability

A well-organized directory structure reduces software complexity over time.

Clear separation between code, documentation, configuration and scientific products enables efficient maintenance by future contributors.

---

# 46. Future Repository Evolution

As Globe-CitySpace evolves, new directories may be introduced without altering the existing organizational philosophy.

The repository structure is intended to support future research areas, new scientific modules and additional visualization capabilities.

---

# 47. Chapter Conclusion

A consistent directory organization is essential for large scientific software projects.

The Globe-CitySpace repository structure has been designed to facilitate collaboration, reproducibility, maintenance and long-term research development.

---

# 48. Next Chapter

Continue with:

**Chapter 05 — Scientific Data**

---

===========================================================
END OF DOCUMENT
===========================================================