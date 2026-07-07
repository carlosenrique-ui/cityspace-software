# Globe-CitySpace Engineering Handbook

---

# Chapter 00

# Executive Summary

**Version:** 2.0

**Project:** Globe-CitySpace

**Institution:** Institute for Technological Research (IPT)

**Location:** São Paulo, Brazil

---

# Purpose of this Handbook

The Globe-CitySpace Engineering Handbook is the official technical documentation of the Globe-CitySpace platform.

Its objective is to preserve the technical knowledge accumulated during the project and provide a complete reference for developers, researchers, students and future maintainers.

This handbook complements the project's README and should be considered the primary engineering documentation of the platform.

---

# About Globe-CitySpace

Globe-CitySpace is a multi-scale geospatial platform capable of transforming any location on Earth into a scientific, interactive and tangible urban model.

The platform integrates global visualization, scientific raster processing, Digital Twin technologies and tangible interfaces into a single engineering workflow.

The system was designed to support research in:

- Urban Digital Twins
- Smart Cities
- Scientific Visualization
- Geospatial Artificial Intelligence
- Urban Planning
- Carbon Neutral Cities
- Projection Mapping
- GIS

---

# Engineering Philosophy

The project follows five fundamental principles.

## 1. Scientific Reproducibility

All scientific products should be reproducible.

The same input data must always generate the same outputs.

---

## 2. Modular Architecture

Each subsystem has a well-defined responsibility.

Major components can evolve independently.

---

## 3. Separation Between Software and Scientific Data

Source code and scientific datasets are maintained independently.

Software is versioned using GitHub.

Scientific datasets are maintained in the institutional repository.

---

## 4. Multi-Scale Design

The platform was designed to support different cartographic scales.

The same workflow can be applied from neighborhood analysis to city-scale visualization.

---

## 5. Extensibility

New cities, datasets, algorithms and visualization modules should be incorporated with minimal impact on the existing architecture.

---

# Project Overview

The engineering workflow is summarized below.

```text
Globe-CitySpace

        │

Latitude / Longitude

        │

Area of Interest (AOI)

        │

Scientific Raster Pipeline

        │

Scientific Products

        │

IPT-CitySpace

        │

Projection Mapping

        │

Virtual Table

        │

Physical Table
```

---

# Main Software Components

The platform is organized into four major subsystems.

## Globe-CitySpace

Responsible for:

- global navigation;
- city selection;
- area definition;
- cartographic visualization.

---

## Offline Scientific Pipeline

Responsible for:

- DSM processing;
- DTM processing;
- raster analysis;
- scientific grid generation;
- metadata generation;
- scientific products.

---

## IPT-CitySpace

Responsible for:

- projection mapping;
- scientific visualization;
- integration with the tangible interface.

---

## Virtual Table

Responsible for:

- virtual simulation;
- actuator validation;
- interaction with the physical table.

---

# Scientific Data

Large scientific datasets are intentionally maintained outside the Git repository.

Typical datasets include:

- DSM
- DTM
- Height Maps
- BMP Products
- CSV Products
- Scientific Snapshots

This separation keeps the software repository lightweight while allowing scientific datasets to evolve independently.

---

# Documentation Organization

Project documentation is organized into the following sections.

```text
README.md

Developer Handbook

Architecture

Development

Releases

Reverse Engineering

Roadmaps
```

Each document has a specific purpose.

The README introduces the project.

The Engineering Handbook documents the complete software platform.

Architecture documents describe design decisions.

Development documents record implementation details.

Release documents preserve project history.

Reverse Engineering documents register technical investigations performed during development.

---

# Intended Audience

This handbook is intended for:

- software developers;
- GIS specialists;
- researchers;
- graduate students;
- scientific collaborators;
- future maintainers of the platform.

No previous knowledge of the project is assumed.

---

# Recommended Reading Order

New contributors are encouraged to read the documentation in the following order.

1. README

2. Executive Summary

3. Introduction

4. System Architecture

5. Development Environment

6. Directory Structure

7. Scientific Data

8. Offline Pipeline

9. Globe-CitySpace

10. IPT-CitySpace

11. Virtual Table

12. GitHub and Teams

13. Backup and Recovery

14. Roadmap

---

# Software Repository

The official source code repository contains only software and documentation.

Large scientific datasets are maintained separately by the project team.

This approach improves maintainability, reduces repository size and simplifies version control.

---

# Long-Term Vision

Globe-CitySpace aims to become an extensible engineering platform for the development of Urban Digital Twins capable of integrating global geospatial visualization, scientific processing and tangible interfaces into a unified workflow.

The platform is expected to support future research, technology transfer and collaboration between academia, government and industry.

---

# Next Chapter

Continue with:

**Chapter 01 — Introduction**