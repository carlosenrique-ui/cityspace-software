# Globe-CitySpace

> **An Open-Source Platform for Multi-Scale Urban Digital Twins, Geospatial Exploration and Tangible City Modeling**

Developed at the **Institute for Technological Research (IPT)**, São Paulo, Brazil.

---

## Overview

Globe-CitySpace is an open-source geospatial platform designed to transform any location on Earth into a scientific, interactive, and tangible urban model.

The platform integrates:

- 🌍 Global 3D visualization
- 📍 Latitude / Longitude navigation
- 🏙 City selection
- 🗺 Cartographic grid generation
- ⛰ Terrain and building height extraction
- 📊 Scientific raster processing
- 🎛 IPT-CitySpace integration
- 🧩 Projection Mapping
- 🏗 Virtual and Physical Tangible Tables

The project supports research in **Urban Digital Twins**, **Smart Cities**, **Geospatial Artificial Intelligence**, and **Carbon Neutral Cities**.

---

# Features

## Globe Navigation

- Global 3D visualization
- CesiumJS interface
- ESRI imagery
- City catalog
- Latitude / Longitude navigation

## Area Selection

Users can define an Area of Interest (AOI) anywhere on Earth.

The selected region becomes a **CitySpace Area**, which serves as the input for the scientific processing pipeline.

## Scientific Raster Pipeline

The platform automatically generates:

- Cartographic grids
- Terrain models
- Building models
- Height maps
- Gray-scale maps
- Scientific metadata
- CSV outputs
- BMP outputs

## IPT-CitySpace Integration

The Globe-CitySpace platform is fully integrated with IPT-CitySpace, enabling:

- Projection Mapping
- Virtual Tangible Table
- Physical Tangible Table
- Scientific Visualization
- Digital Twin experimentation

---

# System Architecture

```
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

# Project Structure

```
globe_cityspace_open/
│
├── frontend/
├── backend/
├── docs/
│
offline/
online/
runner/
config/
│
Dockerfile
docker-compose.yml
requirements-docker.txt
start_demo.sh
start_demo2.sh
README.md
```

---

# Technologies

- Python
- JavaScript
- CesiumJS
- Docker
- Dash
- GDAL
- Rasterio
- NumPy
- OpenStreetMap
- ESRI World Imagery

---

# Running the Demo

## Requirements

- Docker Desktop
- Docker Compose
- Python 3.11+
- Conda
- geo_env_2018

## Start

```bash
./start_demo2.sh
```

---

## Services

| Service | URL |
|----------|-----|
| Globe-CitySpace | http://localhost:8088 |
| IPT-CitySpace | http://localhost:8050 |
| Virtual Table | http://localhost:8060 |

---

# Scientific Workflow

```
City
   │
Latitude / Longitude
   │
Area Selection
   │
Scientific Pipeline
   │
Terrain + Buildings
   │
Cartographic Grid
   │
BMP / CSV
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
- BMP files
- CSV files
- Metadata
- Scientific Reports

---

# Data Policy

Large scientific datasets are **not included** in this repository.

Examples include:

- DSM
- DTM
- Height Maps
- BMP outputs
- CSV outputs
- Scientific snapshots

These datasets are maintained separately because of their size.

---

# Research Areas

- Urban Digital Twins
- Smart Cities
- Geospatial AI
- Urban Planning
- GIS
- Projection Mapping
- Urban Simulation
- Environmental Monitoring
- Carbon Neutral Cities

---

# Roadmap

Future developments include:

- Multi-scale global navigation
- Automated scientific raster pipeline
- AI-assisted geospatial analysis
- Advanced Digital Twin generation
- Municipal Spatial Data Infrastructure (SDI) integration
- Carbon Neutral City applications

---

# Contributing

Contributions are welcome.

Please use GitHub Issues for:

- Bug reports
- Feature requests
- Documentation improvements
- Scientific enhancements

---

# License

This repository contains research software developed at the **Institute for Technological Research (IPT)**.

Please refer to the project license before redistribution or commercial use.

---

# Author

**Carlos Enrique Hernandez Simoes**

Institute for Technological Research (IPT)

São Paulo, Brazil

---

# Acknowledgements

This project builds upon the open-source geospatial ecosystem, including:

- CesiumJS
- GDAL
- Rasterio
- NumPy
- OpenStreetMap
- Dash
- Python