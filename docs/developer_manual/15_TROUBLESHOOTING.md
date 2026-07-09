# Globe-CitySpace Engineering Handbook

# Chapter 15 — Troubleshooting

---

## 1. Purpose

This chapter provides guidance for diagnosing and resolving the most common issues encountered during the installation, configuration and operation of Globe-CitySpace.

Its objectives are to:

- reduce debugging time;
- provide standardized troubleshooting procedures;
- simplify maintenance;
- preserve engineering knowledge;
- support future developers.

Whenever possible, developers should identify the root cause before applying corrective actions.

---

## 2. Troubleshooting Strategy

Problems should always be investigated in the following order:

1. Verify the execution environment.
2. Verify software dependencies.
3. Verify project configuration.
4. Verify scientific input data.
5. Verify generated outputs.
6. Verify synchronization between software components.

This structured approach minimizes unnecessary debugging efforts.

---

## 3. Docker Container Does Not Start

### Symptoms

- Docker container exits immediately.
- Browser cannot connect.
- HTTP service unavailable.

### Possible Causes

- Docker Desktop is not running.
- Required ports are already in use.
- Missing Docker image.
- Invalid Docker Compose configuration.

### Recommended Actions

- Verify Docker Desktop is running.
- Execute:

```bash
docker compose ps
```

- Inspect container logs:

```bash
docker compose logs
```

- Restart the environment:

```bash
docker compose down
docker compose up --build
```

---

## 4. Python Environment Problems

### Symptoms

- Python modules cannot be imported.
- Conda environment not found.
- Runtime errors during startup.

### Recommended Actions

Verify the active environment:

```bash
conda info --envs
```

Activate the correct environment:

```bash
conda activate <environment_name>
```

Verify Python version:

```bash
python --version
```

Install missing dependencies if required.

---

## 5. Browser Cannot Open Globe-CitySpace

### Symptoms

- Blank page.
- Connection refused.
- HTTP timeout.

### Possible Causes

- Web server not running.
- Incorrect port.
- Firewall restrictions.
- Browser cache.

### Recommended Actions

Verify the HTTP server.

Confirm the configured port.

Clear browser cache.

Restart the application if necessary.

---

## 6. Cesium Does Not Load

### Symptoms

- Empty globe.
- Missing terrain.
- Missing imagery.
- JavaScript errors.

### Possible Causes

- Invalid Cesium token.
- Internet connection unavailable.
- Incorrect asset configuration.
- Browser security restrictions.

### Recommended Actions

Verify:

- Cesium access token.
- Internet connectivity.
- Browser console messages.
- Asset URLs.

Reload the application after correcting the configuration.

---

## 7. Scientific Raster Is Missing

### Symptoms

- No raster displayed.
- Empty scientific products.
- Missing BMP files.

### Possible Causes

- Offline Pipeline not executed.
- Invalid raster source.
- Incorrect output directory.
- Processing interrupted.

### Recommended Actions

Verify:

- raster input files;
- processing logs;
- output directories;
- metadata generation.

Execute the Offline Pipeline again if necessary.

---

## 8. Grid Does Not Match Projection

### Symptoms

- Grid shifted.
- Projection misaligned.
- Cells do not correspond to projected imagery.

### Possible Causes

- Incorrect Bounding Box.
- Wrong coordinate transformation.
- Invalid Project Rotation Angle.
- Metadata mismatch.

### Recommended Actions

Verify:

- Bounding Box;
- CRS;
- centroid coordinates;
- Project Rotation Angle;
- generated metadata.

The projection should always use the same metadata generated during the Offline Pipeline.

---

## 9. Wrong Project Rotation

### Symptoms

- Roads are not parallel to the engineering grid.
- Projection appears rotated incorrectly.
- North arrow does not match the expected orientation.

### Possible Causes

- Incorrect rotation selected during exploration.
- Rotation not stored in project metadata.
- Metadata not propagated to IPT-CitySpace.

### Recommended Actions

Return to the exploration phase.

Select the correct Project Rotation Angle.

Regenerate all scientific products.

Never modify the rotation manually after the Offline Pipeline has completed.

---

## 10. North Arrow Is Incorrect

### Symptoms

- North arrow points in the wrong direction.
- Geographic north appears inconsistent.

### Possible Causes

- Missing Project Rotation Angle.
- Incorrect metadata.
- Rendering configuration error.

### Recommended Actions

Verify that the north arrow is computed from the stored Project Rotation Angle rather than assuming alignment with the engineering Y-axis.

This guarantees consistency between Globe-CitySpace, IPT-CitySpace and the Physical Table.

---

## 11. Virtual Table Does Not Synchronize

### Symptoms

- Virtual Table remains static.
- Actuators do not update.
- Projection does not follow simulation.

### Possible Causes

- Synchronization service not running.
- Invalid communication channel.
- Missing scientific products.
- Metadata inconsistency.

### Recommended Actions

Verify:

- synchronization service;
- communication logs;
- actuator mapping;
- metadata files.

Restart synchronization after correcting the identified issue.

---

## 12. Physical Table Does Not Respond

### Symptoms

- No actuator movement.
- Partial actuator response.
- Delayed physical updates.

### Possible Causes

- Hardware communication failure.
- Power supply problems.
- Controller malfunction.
- Invalid actuator mapping.

### Recommended Actions

Verify:

- hardware power;
- controller status;
- communication interface;
- actuator addressing.

Always validate the project using the Virtual Table before testing the Physical Table.

---

## 13. BMP File Is Not Generated

### Symptoms

- Missing BMP output.
- Projection Mapping unavailable.
- Export step fails.

### Possible Causes

- Raster generation failure.
- Invalid output directory.
- File permission issues.
- Interrupted processing.

### Recommended Actions

Verify:

- output directory;
- write permissions;
- raster generation logs;
- metadata completeness.

Execute the export stage again after resolving the problem.

---

## 14. CSV Export Is Incorrect

### Symptoms

- Missing values.
- Invalid coordinates.
- Wrong elevations.
- Incorrect actuator identifiers.

### Possible Causes

- Metadata mismatch.
- Grid generation failure.
- Coordinate transformation error.

### Recommended Actions

Inspect:

- generated CSV files;
- engineering grid;
- centroid coordinates;
- Project Rotation Angle;
- metadata consistency.

---

## 15. Terrain Heights Are Incorrect

### Symptoms

- Terrain appears too high.
- Terrain appears too low.
- Unexpected discontinuities.

### Possible Causes

- Wrong DEM source.
- Incorrect raster resolution.
- CRS conversion problems.
- Sampling error.

### Recommended Actions

Verify:

- DEM source;
- raster resolution;
- CRS transformation;
- centroid sampling process.

Regenerate the scientific products after correcting the terrain source.

---

## 16. Building Heights Are Incorrect

### Symptoms

- Buildings appear too tall.
- Buildings appear too short.
- Missing buildings.
- Incorrect roof elevations.

### Possible Causes

- Incorrect building dataset.
- Invalid building footprints.
- Wrong elevation source.
- Processing configuration error.

### Recommended Actions

Verify:

- building source;
- footprint integrity;
- building height model;
- processing parameters.

Reprocess the engineering products if necessary.

---

## 17. Projection Mapping Is Misaligned

### Symptoms

- Projected image shifted.
- Colors do not match the physical surface.
- Grid and image are offset.

### Possible Causes

- Incorrect projector calibration.
- Invalid projection geometry.
- Rotation mismatch.
- Wrong table dimensions.

### Recommended Actions

Verify:

- projector calibration;
- table dimensions;
- Project Rotation Angle;
- projection metadata.

Repeat the projection calibration procedure if required.

---

## 18. Coordinate System Problems

### Symptoms

- Geographic position is incorrect.
- Grid displaced.
- Imported datasets do not align.

### Possible Causes

- Wrong Coordinate Reference System (CRS).
- Incorrect EPSG code.
- Coordinate transformation failure.

### Recommended Actions

Confirm:

- source CRS;
- destination CRS;
- EPSG identifiers;
- transformation parameters.

All datasets must use compatible coordinate systems before processing.

---

## 19. Metadata Inconsistency

### Symptoms

- Different modules produce incompatible outputs.
- Grid dimensions differ.
- Rotation values are inconsistent.

### Possible Causes

- Metadata manually modified.
- Partial pipeline execution.
- Outdated configuration files.

### Recommended Actions

Never edit metadata files manually.

Regenerate the metadata through the Offline Pipeline and verify that all modules reference the same project configuration.

---

## 20. Performance Issues

### Symptoms

- Slow processing.
- Long loading times.
- Delayed visualization.
- Reduced responsiveness.

### Possible Causes

- Large raster datasets.
- Insufficient memory.
- Slow storage devices.
- Excessive browser cache.

### Recommended Actions

Verify:

- available RAM;
- disk performance;
- browser cache;
- raster resolution.

Reduce dataset size for debugging whenever possible before processing the complete project.

---

## 21. Logging and Debugging

### Recommendation

Whenever an unexpected behavior occurs, collect diagnostic information before modifying the software.

Useful information includes:

- execution logs;
- Python exceptions;
- browser console messages;
- Docker logs;
- processing timestamps;
- metadata files.

Maintaining complete logs significantly reduces debugging time.

---

## 22. Recommended Verification Sequence

When investigating a problem, follow this order:

1. Verify the execution environment.
2. Verify Docker or Conda.
3. Verify configuration files.
4. Verify input datasets.
5. Verify metadata.
6. Verify generated outputs.
7. Verify visualization.
8. Verify synchronization.
9. Verify hardware.

Following a fixed sequence prevents unnecessary troubleshooting steps.

---

## 23. Common Engineering Mistakes

The following mistakes are among the most frequent:

- Using an incorrect CRS.
- Forgetting to regenerate metadata.
- Changing the Project Rotation Angle after processing.
- Editing generated CSV files manually.
- Using outdated raster datasets.
- Skipping the Offline Pipeline.
- Testing directly on the Physical Table without validating the Virtual Table.

Avoiding these mistakes greatly improves system reliability.

---

## 24. Before Reporting a Bug

Before opening an issue or requesting technical support, verify that:

- Docker containers are running.
- Required services are available.
- Scientific products were successfully generated.
- Metadata is complete.
- The Project Rotation Angle is correct.
- The correct engineering scale was used.
- The problem can be reproduced.

Providing this information accelerates problem diagnosis.

---

## 25. Troubleshooting Philosophy

Troubleshooting should prioritize identifying the root cause rather than applying temporary fixes.

Whenever a recurring issue is discovered:

- document it;
- identify its origin;
- correct the underlying cause;
- update this handbook if necessary.

Continuous improvement of troubleshooting documentation benefits all future developers.

---

## 26. Preventive Maintenance

Preventive maintenance reduces the occurrence of operational problems.

Recommended activities include:

- updating project documentation;
- validating engineering contracts;
- testing Docker environments;
- verifying software dependencies;
- checking scientific datasets;
- reviewing backup procedures.

Regular maintenance improves long-term system stability.

---

## 27. Recovery Checklist

Before resuming normal operation, verify that:

- all required services are running;
- the engineering environment is correctly configured;
- scientific products are available;
- metadata is complete and consistent;
- visualization is operational;
- synchronization has been validated;
- hardware communication is functioning correctly.

This checklist should be completed before every major demonstration.

---

## 28. Engineering Support Philosophy

Troubleshooting should always follow engineering principles.

Problems should be:

- reproduced;
- documented;
- analyzed;
- corrected;
- validated.

Corrective actions should eliminate the underlying cause rather than only the observed symptom.

---

## 29. Chapter Summary

This chapter documents the most common operational problems that may occur during the installation, execution and maintenance of Globe-CitySpace.

It provides standardized procedures for diagnosing issues related to:

- software configuration;
- scientific processing;
- engineering visualization;
- synchronization;
- Projection Mapping;
- Virtual Table;
- Physical Table.

Following these procedures improves system reliability, reduces debugging time and facilitates long-term maintenance.

---

# Next Chapter

**Chapter 16 — Contributing**

---

===========================================================

END OF DOCUMENT

===========================================================