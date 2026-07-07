# Globe-CitySpace Engineering Handbook

---

# Chapter 01

# Introduction

**Version:** 2.0

**Project:** Globe-CitySpace

**Institution:** Institute for Technological Research (IPT)

**Location:** São Paulo, Brazil

---

# Purpose

This document introduces the Globe-CitySpace platform and presents the engineering concepts that guided its development.

It explains why the project was created, the problems it addresses, its intended applications, and the overall philosophy behind the software architecture.

This chapter should be read before any technical chapter of this handbook.

---

# Background

Urban environments are becoming increasingly complex.

Modern cities continuously generate large amounts of geographic, environmental, transportation and infrastructure data.

Although these datasets are becoming more accessible, transforming them into useful information for planning and decision-making remains a significant challenge.

Traditional Geographic Information Systems (GIS) are extremely powerful for visualization and spatial analysis but are often disconnected from physical interaction and tangible interfaces.

At the same time, Digital Twin technologies have demonstrated that interactive representations of real-world environments can significantly improve urban planning, simulation and decision support.

Globe-CitySpace was conceived to bridge these two worlds.

---

# Motivation

The project originated from the need to create a flexible platform capable of converting geographic information into tangible scientific models.

Rather than focusing exclusively on visualization, the platform was designed to integrate the complete engineering workflow, from global geographic exploration to physical interaction through projection mapping and tangible tables.

This approach allows researchers and decision makers to move naturally between digital analysis and physical interaction.

---

# Vision

The long-term vision of Globe-CitySpace is to provide a reusable engineering platform for creating Urban Digital Twins at multiple cartographic scales.

Instead of being limited to a specific city or dataset, the platform is intended to operate anywhere on Earth whenever compatible geographic information is available.

The same workflow should be applicable to neighborhoods, municipalities, metropolitan regions or entire countries.

---

# Project Objectives

The primary objectives of the project are:

- provide a global geospatial exploration platform;
- support multi-scale urban analysis;
- automate scientific raster processing;
- generate reproducible scientific products;
- integrate Digital Twin technologies;
- support projection mapping;
- operate tangible interfaces;
- facilitate research and technology transfer.

---

# Engineering Approach

Globe-CitySpace was designed as an engineering platform rather than a single software application.

Each subsystem performs a specific responsibility while remaining loosely coupled to the others.

This modular approach allows new capabilities to be incorporated without requiring extensive modifications to the existing software.

---

# Core Principles

The project follows several engineering principles.

## Scientific Reproducibility

Scientific processing must always produce deterministic results.

Given the same input data, identical outputs should be generated.

---

## Modularity

Subsystems should remain independent whenever possible.

New modules should integrate through clearly defined interfaces.

---

## Separation of Responsibilities

Visualization, scientific processing, runtime execution and documentation are maintained as independent components.

This separation simplifies maintenance and encourages software reuse.

---

## Extensibility

The platform should evolve continuously.

New cities, new algorithms, new raster products and new visualization techniques should be incorporated with minimal impact on the existing architecture.

---

## Maintainability

Long-term maintenance is considered part of the software design.

Documentation, version control and engineering practices receive the same attention as source code.

---

# System Overview

The platform is organized into four major engineering domains.

```text
                Globe-CitySpace

        Global Geographic Exploration

                     │

                     ▼

           Area of Interest (AOI)

                     │

                     ▼

       Offline Scientific Processing

                     │

                     ▼

         Scientific Raster Products

                     │

                     ▼

             IPT-CitySpace Runtime

                     │

          Projection Mapping Engine

                     │

          Virtual Tangible Interface

                     │

          Physical Tangible Interface
```

---

# Main Components

The engineering workflow is composed of four major software components.

## Globe-CitySpace

Responsible for global navigation, city selection, geographic exploration and area definition.

---

## Offline Scientific Pipeline

Responsible for scientific raster processing, grid generation, terrain analysis and production of engineering outputs.

---

## IPT-CitySpace

Responsible for runtime visualization, projection mapping and integration with the tangible interface.

---

## Virtual Table

Responsible for simulation, actuator validation and interaction with the physical table.

---

# Scientific Processing

Scientific processing transforms raw geographic information into engineering products.

Typical products include:

- cartographic grids;
- terrain models;
- surface models;
- building heights;
- scientific metadata;
- CSV datasets;
- BMP datasets;
- projection mapping inputs.

These products constitute the interface between the scientific pipeline and the runtime system.

---

# Multi-Scale Concept

One of the distinguishing characteristics of Globe-CitySpace is its multi-scale design.

The platform was conceived to support analyses ranging from local neighborhoods to complete urban regions.

Different cartographic scales can therefore share the same engineering workflow while relying on different geographic datasets.

---

# Scientific Data

The project distinguishes software from scientific data.

Software components are maintained under version control.

Scientific datasets are maintained independently because of their size and update frequency.

This separation reduces repository size while preserving reproducibility.

---

# Documentation Strategy

The project documentation is organized into complementary layers.

```text
README

Engineering Handbook

Architecture Documents

Development Notes

Release Notes

Reverse Engineering

Scientific Documentation
```

Each document serves a specific purpose and avoids unnecessary duplication.

---

# Intended Audience

This handbook is intended for:

- software developers;
- GIS specialists;
- researchers;
- graduate students;
- scientific collaborators;
- future maintainers.

The documentation assumes general software development knowledge but does not require previous familiarity with Globe-CitySpace.

---

# Engineering Lifecycle

The typical engineering lifecycle adopted by the project is:

```text
Requirements

↓

Architecture

↓

Implementation

↓

Scientific Processing

↓

Validation

↓

Projection Mapping

↓

Virtual Simulation

↓

Physical Demonstration

↓

Documentation

↓

Release
```

---

# Future Directions

Future work includes:

- automated global data acquisition;
- advanced Digital Twin generation;
- AI-assisted geographic analysis;
- integration with municipal SDIs;
- additional tangible interfaces;
- support for new scientific datasets;
- cloud-native execution.

---

# Summary

Globe-CitySpace combines geospatial visualization, scientific raster processing and tangible interaction into a unified engineering platform.

Its modular architecture allows continuous evolution while preserving reproducibility, maintainability and scientific rigor.

The following chapters describe each subsystem in detail.

---

# Next Chapter

**Chapter 02 — System Architecture**