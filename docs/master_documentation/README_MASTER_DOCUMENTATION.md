# IPT-CitySpace
# Engineering Master Documentation

Version: Initial Master Documentation
Status: Living Architectural Document

---

# Objective

This documentation consolidates the architectural, scientific,
geospatial, runtime, operational and conceptual foundations of the
IPT-CitySpace platform.

The purpose is to preserve the engineering memory of the system and
provide a stable long-term reference for:

- research
- development
- scientific reproducibility
- architectural continuity
- onboarding
- reverse engineering
- operational evolution
- digital twin evolution
- tangible table integration
- adaptive urban systems
- future 3D/Cesium integration

---

# Documentation Philosophy

The IPT-CitySpace architecture follows a strict separation between:

- OFFLINE scientific processing
- ONLINE runtime consumption
- UI visualization
- physical tangible table synchronization

The ONLINE runtime must never recompute scientific processing.

Scientific processing belongs exclusively to the OFFLINE layer.

---

# High-Level Concept

The platform represents an experimental Urban Digital Twin system
capable of integrating:

- geospatial scientific processing
- terrain modeling
- urban semantic transformation
- runtime synchronization
- tangible interfaces
- temporal urban visualization
- operational dashboards
- future real-time streaming
- future urban simulation systems

---

# Core Architectural Principles

## Deterministic Architecture

The pipeline is deterministic.

The same scientific inputs must generate the same runtime products.

---

## Contract-Oriented Engineering

The system relies heavily on:

- file contracts
- artifact contracts
- runtime contracts
- scientific validation contracts

Artifacts are treated as canonical interfaces between layers.

---

## Offline/Online Separation

The architecture strictly separates:

### OFFLINE

Responsible for:

- DSM/DTM processing
- scientific raster processing
- CRS normalization
- grid computation
- PCA alignment
- semantic transformation
- contour generation
- runtime artifact generation

### ONLINE

Responsible for:

- runtime synchronization
- visualization
- event execution
- temporal navigation
- UI rendering
- actuator simulation

ONLINE must consume OFFLINE artifacts without scientific recomputation.

---

# System Layers

## Layer 1 — Scientific Geospatial Processing

Scientific layer responsible for:

- raster processing
- vector processing
- spatial normalization
- coordinate transformation
- scientific validation

Main technologies:

- GeoPandas
- Rasterio
- GDAL
- NumPy
- Shapely
- Pyogrio
- Pandas

---

## Layer 2 — Semantic Transformation

Responsible for converting scientific outputs into semantic runtime data.

Examples:

- grid metrics
- semantic layers
- runtime metadata
- actuator representations

---

## Layer 3 — Runtime Artifacts

Artifacts generated offline and consumed online.

Examples:

- grid_metrics_utm.csv
- grid.npy
- actuator_plan.json
- metadata.json
- semantic overlays
- contours
- watermarks

---

## Layer 4 — ONLINE Runtime Engine

Responsible for:

- timeline control
- synchronization
- traversal simulation
- runtime execution
- temporal orchestration

Core concepts:

- EventBus
- TemporalConductor
- StateManager
- PlanExecutionRunner

---

## Layer 5 — ONLINE/UI

Responsible for:

- Dash UI
- Plotly rendering
- virtual tangible table
- overlays
- heatmaps
- contours
- synchronization visualization

---

# Scientific Geospatial Concepts

## DSM / DTM

DSM:
Digital Surface Model.

DTM:
Digital Terrain Model.

The platform uses both models for:

- terrain reconstruction
- urban elevation modeling
- semantic height computation

---

## Scientific Grid

The system generates a scientific grid over the study domain.

Grid characteristics:

- deterministic
- metric
- georeferenced
- aligned with scientific CRS

The grid is later transformed into runtime/tangible coordinates.

---

## CRS

Primary CRS detected:

EPSG:31983
SIRGAS 2000 / UTM Zone 23S

---

## PCA Rotation

The architecture uses PCA-based validation and alignment.

PCA is used for:

- alignment validation
- rotation consistency
- scientific orientation
- tangible table alignment

---

# Tangible Table Concepts

## Physical Grid

Current prototype:

- 16 x 8 grid
- 128 actuators/pins

Future architecture:

- generalized M x N grid

---

## Tangible Synchronization

The virtual and physical tables are expected to operate synchronously.

Future synchronization modes:

- virtual-only
- physical-only
- hybrid synchronized mode

---

## Runtime Traversal

The runtime currently simulates zigzag traversal across the grid.

The traversal model is related to:

- actuator motion
- XY movement
- timing estimation
- synchronization physics

---

# Runtime Physics Concepts

The runtime architecture considers:

- height-dependent timing
- XY movement timing
- traversal synchronization
- actuator execution ordering

The runtime is expected to evolve into a physically calibrated execution engine.

---

# Event-Driven Runtime

The runtime architecture is event-driven.

Core concepts detected:

- event queues
- runtime clocks
- traversal execution
- state synchronization
- deterministic replay

---

# Semantic Transformation Layer

The semantic layer converts scientific geospatial information into
runtime-operational representations.

Examples:

- actuator heights
- semantic overlays
- runtime metrics
- visual semantic layers

---

# Reverse Engineering Findings

The reverse engineering phases revealed:

- deterministic scientific chain
- wrapper/delegated scripts
- contract-driven architecture
- static artifact generation
- controlled subprocess execution
- absence of unresolved dynamic chains

---

# Controlled Risks

Detected controlled risks:

- wrapper delegation resolved
- subprocess usage isolated
- no unresolved runpy execution
- stable offline contracts

---

# Remaining Risks

Potential risks:

- strong dependency on file contracts
- hidden assumptions in datasets
- strict artifact consistency requirements
- runtime dependency on canonical products

---

# Future Evolution

## Cesium Integration

Future possibilities:

- 3D terrain
- streaming terrain
- urban digital twin
- real-time synchronization

---

## Adaptive Urban Twin

Long-term vision:

- dynamic city synchronization
- streaming urban data
- adaptive runtime behavior
- operational city simulation
- carbon-neutral city modeling

---

## Traffic and Urban Simulation

Potential future integrations:

- CMEM
- VSP
- VISUM/VISSIM
- urban traffic simulation
- emission modeling
- carbon estimation

---

# Carbon-Neutral City Vision

The platform is evolving toward:

- environmental simulation
- urban sustainability
- operational decision support
- urban resilience analysis
- carbon-aware planning

---

# Architectural Identity

The IPT-CitySpace architecture already demonstrates characteristics of:

- Urban Digital Twin
- Adaptive Urban Runtime
- Scientific Geospatial Platform
- Tangible Urban Interface
- Hybrid Offline/Online Runtime System

---

# Engineering Philosophy

The project evolved through iterative engineering cycles involving:

- reverse engineering
- architectural stabilization
- scientific validation
- runtime experimentation
- UI evolution
- geospatial validation
- synchronization experiments

The architecture preserves deterministic scientific processing while
allowing progressive runtime evolution.

---

# Documentation Status

This document is a living architectural reference.

Future chapters may include:

- diagrams
- temporal models
- runtime state machines
- actuator protocols
- Cesium integration
- streaming architecture
- hardware integration
- calibration systems
- adaptive synchronization
- AI-assisted urban systems

