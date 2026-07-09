# Globe-CitySpace

## Open Geospatial Platform for Urban Digital Twins

Developed at the **Institute for Technological Research (IPT)**, São Paulo, Brazil.

---

# Mission

Globe-CitySpace is an extensible geospatial platform for building multi-scale Urban Digital Twins through global visualization, scientific raster processing, and tangible interfaces.

The platform integrates geospatial technologies, scientific processing pipelines, and projection mapping to support research, education, planning, simulation, and decision-making.

---

# Overview

Globe-CitySpace transforms any location on Earth into a scientific and interactive urban model.

The platform combines:

- 🌍 Global 3D visualization
- 📍 Latitude / Longitude navigation
- 🏙 City selection
- 🗺 Cartographic grid generation
- ⛰ Terrain and building height extraction
- 📊 Scientific raster processing
- 🎛 IPT-CitySpace integration
- 🧩 Projection Mapping
- 🏗 Virtual and Physical Tangible Tables

The project supports research in:

- Urban Digital Twins
- Smart Cities
- Geospatial Artificial Intelligence
- Carbon Neutral Cities
- Urban Planning
- Scientific Visualization

---

# Quick Start

## Requirements

- Windows 10 / 11
- WSL2
- Ubuntu
- Visual Studio Code
- Docker Desktop
- Docker Compose
- Python 3.11+
- Conda
- Conda Environment: `geo_env_2018`

## Running the Demonstration

> Scientific datasets are maintained separately from this repository.

```bash
./start_demo2.sh
```

After startup:

| Service | URL |
|----------|-----|
| Globe-CitySpace | http://localhost:8088/demo.html |
| IPT-CitySpace | http://localhost:8050 |
| Virtual Table | http://localhost:8060 |

---

# Core Capabilities

## Globe Navigation

- Global 3D visualization
- CesiumJS interface
- ESRI World Imagery
- City catalog
- Latitude / Longitude navigation

---

## Area Selection

Users can define an Area of Interest (AOI) anywhere on Earth.

The selected region becomes a **CitySpace Area**, serving as the input for the scientific processing pipeline.

---

## Scientific Raster Pipeline

The platform automatically generates:

- Cartographic Grids
- Terrain Models (DTM)
- Surface Models (DSM)
- Building Models
- Height Maps
- Gray-scale Maps
- Scientific Metadata
- CSV Products
- BMP Products

---

## IPT-CitySpace Integration

Globe-CitySpace integrates directly with IPT-CitySpace, enabling:

- Projection Mapping
- Virtual Tangible Table
- Physical Tangible Table
- Scientific Visualization
- Digital Twin experimentation

---

# System Architecture

```text
                 Globe-CitySpace
                        │
                        ▼
            Latitude / Longitude
                        │
                        ▼
             CitySpace Area (AOI)
                        │
                        ▼
         Scientific Raster Pipeline
                        │
      ┌─────────────────┴─────────────────┐
      ▼                                   ▼
 Cartographic Grid               Scientific Products
      │                                   │
      └─────────────────┬─────────────────┘
                        ▼
                  IPT-CitySpace
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
     Virtual Table          Physical Table
```

---

# Repository Structure

```text
globe_cityspace_open/
│
├── frontend/                 User Interface
├── backend/                  Globe Services
├── core/                     Core Components
├── contracts/                System Contracts
├── data/                     Internal Resources
├── docs/                     Module Documentation
└── projects/                 Project Configurations

offline/                      Scientific Processing Pipeline
online/                       Runtime Environment
runner/                       Execution Engine
config/                       System Configuration
scripts/                      Utility Scripts
tests/                        Automated Tests

Dockerfile
docker-compose.yml
requirements-docker.txt
start_demo.sh
start_demo2.sh
README.md
```

---

# Technologies

## Programming Languages

- Python
- JavaScript

## Geospatial Processing

- GDAL
- Rasterio
- NumPy

## Visualization

- CesiumJS
- Dash
- OpenStreetMap
- ESRI World Imagery

## Deployment

- Docker
- Docker Compose
- WSL2
- Ubuntu Linux

---

# Scientific Workflow

```text
City
   │
Latitude / Longitude
   │
Area Selection
   │
Scientific Raster Pipeline
   │
Terrain + Buildings
   │
Cartographic Grid
   │
BMP / CSV Products
   │
Projection Mapping
   │
Virtual Table
   │
Physical Table
```

---

# Generated Products

The scientific pipeline produces:

- Cartographic Grids
- Height Maps
- Gray-scale Maps
- BMP Files
- CSV Files
- Scientific Metadata
- Scientific Reports
- Projection Mapping Products

---

# Scientific Data

Large scientific datasets are **not included** in this repository.

Examples include:

- DSM
- DTM
- Height Maps
- Scientific Rasters
- BMP Products
- CSV Products
- Scientific Snapshots

Scientific datasets are maintained separately in the project's institutional repository.

---

# Documentation

Project documentation is organized as follows:

```text
README.md

docs/developer_manual/
    Globe-CitySpace Engineering Handbook

docs/architecture/
    System Architecture

docs/development/
    Development Notes

docs/releases/
    Release Documentation

docs/reverse_engineering/
    Historical Technical Documentation
```

---

# Research Areas

The platform supports research in:

- Urban Digital Twins
- Smart Cities
- Geographic Information Systems (GIS)
- Geospatial Artificial Intelligence
- Urban Planning
- Projection Mapping
- Environmental Monitoring
- Urban Simulation
- Carbon Neutral Cities

---

# Project Status

**Status:** Active Research and Development

**Version:** 2.x

**Institution:** Institute for Technological Research (IPT)

**Location:** São Paulo, Brazil

---

# Roadmap

Current development focuses on:

- Multi-scale Global Navigation
- Automated Scientific Raster Processing
- AI-assisted Geospatial Analysis
- Advanced Digital Twin Generation
- Municipal Spatial Data Infrastructure (SDI) Integration
- Carbon Neutral City Applications

---

# Contributing

Contributions are welcome.

Please use GitHub Issues for:

- Bug Reports
- Feature Requests
- Documentation Improvements
- Scientific Enhancements

---

# License

This repository contains research software developed at the **Institute for Technological Research (IPT)**.

Please refer to the project license before redistribution or commercial use.

---

# Project Maintainer

**Carlos Enrique Hernandez Simoes**

Institute for Technological Research (IPT)

São Paulo, Brazil

Research Areas:

- Urban Digital Twins
- Geospatial Systems
- Scientific Visualization

---

# Acknowledgements

This project builds upon the open-source geospatial ecosystem, including:

- CesiumJS
- GDAL
- Rasterio
- NumPy
- Dash
- OpenStreetMap
- ESRI World Imagery
- Python

---

# Engineering Handbook

Complete technical documentation is available in:

```text
docs/developer_manual/
```

The Engineering Handbook describes:

- System Architecture
- Development Environment
- Scientific Data Organization
- Offline Scientific Pipeline
- Globe-CitySpace
- IPT-CitySpace
- Virtual Table
- GitHub Workflow
- Microsoft Teams Organization
- Backup and Recovery Procedures
- Project Roadmap
- Glossary
- Architecture Decisions
- Troubleshooting
- Contributing Guidelines