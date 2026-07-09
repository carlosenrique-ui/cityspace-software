# Virtual Table

---

## 1. Purpose

The Virtual Table is the digital representation of the physical actuator table.

Its objective is to reproduce, in software, exactly the same behavior expected from the physical system.

Every actuator displayed on the screen corresponds to one physical actuator.

The Virtual Table is therefore the primary engineering environment used for validation, debugging and demonstration.

---

## 2. Position within the Architecture

The Virtual Table is located after IPT-CitySpace.

The execution sequence is:

Globe-CitySpace

↓

Offline Pipeline

↓

IPT-CitySpace

↓

Virtual Table

↓

Physical Table

↓

Projection Mapping

The Virtual Table acts as the reference model before commands are sent to the real hardware.

---

## 3. Main Responsibilities

The Virtual Table is responsible for:

- reconstructing the actuator matrix;
- displaying actuator heights;
- reproducing actuator motion;
- validating synchronization;
- assisting debugging;
- supporting demonstrations.

Scientific calculations are not performed inside the Virtual Table.

---

## 4. Engineering Representation

Each virtual actuator contains the same engineering information stored in the scientific products.

Typical information includes:

- row;
- column;
- actuator ID;
- terrain height;
- building height;
- total height;
- engineering coordinates.

This guarantees correspondence with the physical actuator.

---

## 5. Engineering Grid

The engineering grid shown in the Virtual Table is identical to the grid generated during Globe-CitySpace exploration.

The following properties remain unchanged:

- dimensions;
- rotation;
- origin;
- spacing;
- indexing.

The grid is never regenerated during operation.

---

## 6. Actuator Matrix

The actuator matrix represents the complete physical table.

Typical configurations include:

- 16 × 8;
- 32 × 16;
- larger future matrices.

Each matrix element corresponds to one actuator position.

---

## 7. Height Representation

Each actuator displays the processed engineering height.

The displayed value corresponds to:

Total Height = Terrain + Building

The Virtual Table never estimates heights.

Instead, it reproduces the scientific values generated previously.

---

## 8. Engineering Rotation

The Virtual Table preserves the project orientation selected during Globe-CitySpace exploration.

The actuator matrix is displayed using the same engineering rotation.

Consequently:

- the engineering grid remains aligned;
- actuator positions remain unchanged;
- projection mapping preserves spatial correspondence;
- the stored rotation angle is never modified.

---

## 9. Coordinate Reference

The Virtual Table inherits the engineering coordinate system from IPT-CitySpace.

Its reference frame includes:

- project centroid;
- engineering origin;
- grid dimensions;
- rotation angle;
- engineering scale.

This guarantees that every virtual actuator represents the same geographic position as its physical counterpart.

---

## 10. Synchronization

The Virtual Table is synchronized continuously with the operational system.

Synchronization includes:

- actuator heights;
- actuator states;
- execution sequence;
- visualization updates.

Every change is immediately reflected on screen.

---

## 11. Actuator States

Each actuator may assume different operational states.

Typical states include:

- idle;
- active;
- moving upward;
- moving downward;
- completed;
- unavailable.

These states simplify monitoring during engineering tests.

---

## 12. Visualization Modes

Different visualization modes may be selected according to the engineering task.

Examples include:

- shaded surface;
- height blocks;
- wireframe grid;
- engineering identifiers;
- colored elevation map.

Changing the visualization mode does not affect actuator behavior.

---

## 13. Engineering Scale

The Virtual Table represents the physical table according to the engineering scale adopted for the project.

The scale controls:

- actuator spacing;
- represented area;
- projected image size;
- engineering measurements.

Scientific values remain independent of the selected visualization scale.

---

## 14. Height Animation

Actuator movement is represented through smooth height animation.

The animation reproduces the commands that will later be executed by the physical hardware.

This behavior allows engineers to verify motion before operating the real actuator table.

---

## 15. Engineering Controls

The Virtual Table provides interactive controls for engineering validation.

Typical controls include:

- Start;
- Stop;
- Pause;
- Resume;
- Reset;
- Step Forward;
- Step Backward.

These controls reproduce the same operational behavior expected from the physical table.

---

## 16. Zigzag Visualization

The actuator traversal order follows the engineering zigzag contract.

The Virtual Table visually displays the activation sequence.

This allows engineers to verify:

- traversal direction;
- actuator numbering;
- synchronization order;
- timing consistency.

The visualization exactly matches the physical implementation.

---

## 17. Projection Synchronization

Projection Mapping remains synchronized with actuator motion.

Whenever actuator heights change:

- the projected raster remains aligned;
- engineering annotations remain fixed;
- image orientation is preserved.

No manual correction is required during operation.

---

## 18. North Reference

The Virtual Table preserves the engineering rotation selected during project creation.

Therefore:

- the engineering grid remains rotated;
- the projected image remains rotated;
- the North Arrow indicates true geographic north.

The North Arrow is displayed only in the 2D engineering visualization.

The 3D environment does not display a fixed "North" label on its Y axis, avoiding ambiguity when the project has been intentionally rotated.

---

## 19. Debugging Environment

The Virtual Table is the preferred environment for engineering debugging.

Typical validation tasks include:

- actuator indexing;
- height verification;
- synchronization testing;
- projection alignment;
- engineering metadata validation.

All debugging can be completed before operating the physical hardware.

---

## 20. Runtime Monitoring

During execution, operational information may be displayed, including:

- current actuator;
- execution step;
- elapsed time;
- synchronization status;
- current project;
- engineering scale.

This information assists engineering supervision during demonstrations and experiments.

---

## 21. Data Integrity

The Virtual Table never modifies the scientific products.

All loaded datasets remain read-only throughout execution.

This guarantees that the validated outputs of the Offline Pipeline are preserved exactly as generated.

---

## 22. Execution Sequence

The Virtual Table follows a deterministic execution sequence.

The operational flow is:

1. Load engineering project.
2. Validate metadata.
3. Initialize actuator matrix.
4. Load projection.
5. Initialize synchronization.
6. Execute actuator sequence.
7. Update visualization.

Every execution follows exactly the same order.

---

## 23. Hardware Independence

The Virtual Table is independent of the physical hardware.

It may operate:

- without actuators;
- with simulated actuators;
- with prototype hardware;
- with the production actuator table.

This characteristic greatly simplifies software development and testing.

---

## 24. Engineering Validation

Before activating the Physical Table, engineers validate:

- engineering rotation;
- actuator numbering;
- projection alignment;
- height distribution;
- synchronization timing;
- visualization consistency.

Only validated projects proceed to physical execution.

---

## 25. Performance Objectives

The Virtual Table has the following engineering objectives:

- smooth animation;
- deterministic execution;
- low latency;
- stable synchronization;
- reproducible operation.

These objectives provide confidence before hardware execution.

---

## 26. Integration with Projection Mapping

The Virtual Table and Projection Mapping share the same engineering reference.

Both components use:

- identical engineering grid;
- identical project rotation;
- identical engineering scale;
- identical actuator positions.

As a result, projected information always coincides with the actuator surface.

---

## 27. Future Expansion

The Virtual Table architecture supports future extensions, including:

- higher actuator densities;
- multiple synchronized tables;
- collaborative operation;
- remote monitoring;
- distributed simulations.

These capabilities can be incorporated without modifying the scientific processing pipeline.

---

## 28. Engineering Advantages

The Virtual Table provides several engineering benefits:

- safe testing;
- repeatable demonstrations;
- hardware-independent validation;
- visualization debugging;
- synchronization verification;
- operator training.

It significantly reduces development risks before deployment to the physical system.

---

## 29. Operational Logging

The Virtual Table records operational events for engineering analysis.

Typical log entries include:

- project loading;
- metadata validation;
- synchronization events;
- actuator commands;
- execution timing;
- warnings;
- errors.

These logs facilitate debugging and performance evaluation.

---

## 30. Engineering Contracts

The Virtual Table follows the same engineering contracts adopted by IPT-CitySpace.

Typical contracts define:

- actuator numbering;
- engineering origin;
- grid dimensions;
- zigzag traversal order;
- maximum actuator stroke;
- engineering scale.

Compliance with these contracts guarantees interoperability with the Physical Table.

---

## 31. Reproducibility

A fundamental requirement of the Virtual Table is reproducibility.

Given the same engineering project, the Virtual Table shall always reproduce:

- identical actuator positions;
- identical heights;
- identical execution order;
- identical visualization.

This property is essential for scientific validation.

---

## 32. Integration with the Physical Table

The Virtual Table serves as the digital counterpart of the Physical Table.

Once the project has been validated, actuator commands can be transmitted directly to the hardware.

Both environments therefore execute the same engineering sequence using the same scientific products.

---

## 33. Operator Support

The Virtual Table assists the operator during demonstrations and engineering tests.

Typical support information includes:

- current execution state;
- active actuator;
- synchronization status;
- engineering scale;
- project identification;
- elapsed execution time.

This information improves operational awareness.

---

## 34. Engineering Philosophy

The Virtual Table is intentionally deterministic.

Every visual element corresponds directly to validated scientific information.

No interpolation, estimation or manual adjustment is introduced during runtime.

This philosophy guarantees that the virtual representation faithfully reproduces the engineering project generated by the Offline Pipeline.

---

## 35. Operational Workflow

The complete Virtual Table workflow is summarized below.

```text
Offline Scientific Products

↓

Load Engineering Project

↓

Validate Metadata

↓

Reconstruct Actuator Matrix

↓

Load Projection Mapping

↓

Initialize Virtual Table

↓

Synchronize Visualization

↓

Execute Actuator Sequence

↓

Engineering Demonstration
```

Each stage preserves the scientific products generated by the Offline Pipeline.

---

## 36. Relationship with the Physical Table

The Virtual Table is the reference implementation of the Physical Table.

Every engineering improvement shall first be validated in the Virtual Table before deployment to the physical hardware.

This development strategy minimizes operational risks and simplifies debugging.

---

## 37. Recommended Workflow

The recommended engineering workflow is:

```text
Globe-CitySpace

↓

Offline Pipeline

↓

Virtual Table Validation

↓

Projection Mapping Validation

↓

Physical Table Validation

↓

Operational Demonstration
```

Only validated engineering projects should reach the Physical Table.

---

## 38. Chapter Summary

The Virtual Table is the engineering validation environment of Globe-CitySpace.

Its responsibilities include:

- loading validated scientific products;
- reconstructing the actuator matrix;
- reproducing actuator movement;
- synchronizing Projection Mapping;
- validating engineering workflows;
- supporting demonstrations.

The Virtual Table guarantees that the Physical Table receives only validated engineering information while preserving the project centroid, engineering grid, Project Rotation Angle and scientific metadata generated during the Offline Pipeline.

---

# Next Chapter

**Chapter 10 — GitHub and Microsoft Teams**

---

===========================================================

END OF DOCUMENT

===========================================================