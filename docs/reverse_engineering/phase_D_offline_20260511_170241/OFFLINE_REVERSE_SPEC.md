# Offline Reverse Specification

Status:
Initial automated reverse inventory.

Purpose:
Map the OFFLINE scientific pipeline before moving to 3D/Cesium.

Rules:
- Do not alter OFFLINE code in this phase.
- Identify canonical runners.
- Identify scientific inputs.
- Identify generated products.
- Identify products consumed by ONLINE.
- Preserve EPSG:31983 scientific CRS.
- Preserve grid semantics: row, col, z_terrain_m, z_building_m, z_total_m.
