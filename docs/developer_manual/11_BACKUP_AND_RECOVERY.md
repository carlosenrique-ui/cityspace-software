# Globe-CitySpace Engineering Handbook

# Chapter 11

# Backup and Recovery

---

## 1. Purpose

This chapter describes the backup and recovery strategy adopted by the Globe-CitySpace engineering platform.

Its objectives are to guarantee:

- preservation of scientific work;
- software reproducibility;
- protection against accidental loss;
- disaster recovery;
- engineering continuity.

The project combines GitHub, Microsoft Teams, local repositories and scientific datasets. Therefore, backup procedures must address all these components.

---

## 2. Philosophy

Backups are based on four principles:

1. Source code must never be lost.

2. Scientific data must always be recoverable.

3. Every released version must be reproducible.

4. Documentation must evolve together with software.

These principles minimize risks during long-term development.

---

## 3. Types of Information

The project contains different categories of information.

### Source Code

Includes:

- Python
- JavaScript
- HTML
- CSS
- configuration files
- Docker
- GitHub Actions
- documentation

Stored primarily on GitHub.

---

### Scientific Data

Includes:

- DEMs
- DSMs
- Orthophotos
- GeoTIFF
- CSV
- Building footprints
- Meshes
- Point clouds
- Experimental datasets

Stored primarily on Microsoft Teams or institutional storage.

---

### Generated Products

Includes:

- BMP files
- PNG images
- CSV outputs
- reports
- screenshots
- temporary products

Usually regenerated when necessary.

Therefore they are generally excluded from Git.

---

## 4. Backup Levels

The Globe-CitySpace project uses multiple backup levels.

Level 1

Developer workstation.

Level 2

Git repository.

Level 3

GitHub remote repository.

Level 4

Microsoft Teams repository.

Level 5

Institutional backups.

Each level protects against different failure scenarios.

---

## 5. GitHub as Primary Backup

GitHub stores:

- software;
- documentation;
- architecture;
- engineering history.

Every commit creates a permanent project history.

Branches protect experimental developments without affecting the stable version.


## 6. Microsoft Teams Backup

Scientific datasets are intentionally separated from the Git repository.

Examples include:

- aerial imagery;
- LiDAR collections;
- DEM repositories;
- orthomosaics;
- municipal datasets;
- large raster files;
- experimental products.

These datasets may occupy several gigabytes or terabytes.

Microsoft Teams provides:

- centralized storage;
- institutional access control;
- version history;
- synchronization;
- sharing among researchers.

---

## 7. Local Backup

Each developer should maintain a complete local copy of the project.

Recommended locations include:

```
C:\workspace\
```

or

```
/mnt/c/workspace/
```

A local repository guarantees that development may continue even without Internet connectivity.

---

## 8. Recommended Directory Layout

Example:

```
workspace/

├── ipt_core_clean/
├── scientific_repository/
├── engineering_inventory/
├── backup/
├── releases/
├── docker_images/
└── archives/
```

Each directory has a specific engineering purpose.

---

## 9. Backup Frequency

Recommended schedule:

Daily

- Git commits
- Local backup

Weekly

- Scientific repository synchronization
- Documentation verification

Monthly

- Complete project archive
- Docker image export
- Release generation

Quarterly

- Disaster recovery validation
- Full repository verification

---

## 10. Git Commit Strategy

Developers should commit frequently.

Good examples:

```
Implemented new DEM loader

Added Globe-CitySpace documentation

Corrected raster rotation

Improved Cesium visualization

Added Docker configuration
```

Poor examples:

```
Update

Changes

Fix

Test

Miscellaneous
```

Clear commit messages simplify future maintenance.


## 11. Branch Protection

Recommended branches:

```
master
```

Stable production version.

```
develop
```

Integration branch.

```
feature/*
```

Development of new features.

```
hotfix/*
```

Emergency corrections.

This organization reduces the probability of introducing unstable code into production.

---

## 12. Release Backup

Every important milestone should generate a release.

Example:

```
v1.0.0

v1.1.0

v2.0.0
```

Each release preserves:

- source code;
- documentation;
- Docker version;
- scientific compatibility;
- engineering state.

---

## 13. Docker Backup

Docker environments should also be preserved.

Recommended commands:

```
docker compose build

docker compose up

docker image ls

docker save
```

Container definitions guarantee identical execution environments across different computers.

---

## 14. Recovery Procedure

If a workstation fails:

Step 1

Install Git.

Step 2

Clone the repository.

```
git clone
```

Step 3

Download scientific datasets.

Step 4

Restore Docker.

Step 5

Install dependencies.

Step 6

Run validation tests.

Step 7

Resume development.

Recovery should require only documented procedures.

---

## 15. Documentation Recovery

The Developer Manual is itself part of the recovery process.

It documents:

- architecture;
- installation;
- execution;
- directory structure;
- scientific pipeline;
- software contracts;
- maintenance procedures.

Without documentation, recovery becomes significantly more difficult.


## 16. Scientific Data Recovery

Scientific repositories should be periodically validated.

Validation includes:

- file integrity;
- coordinate systems;
- raster dimensions;
- metadata consistency;
- directory organization.

Corrupted datasets should be replaced immediately from institutional backups.

---

## 17. Backup Validation

A backup that has never been restored cannot be considered reliable.

Recommended periodic tests:

- clone the repository on a clean machine;
- restore scientific datasets;
- rebuild Docker containers;
- execute the complete pipeline;
- compare generated outputs with reference results.

These validation exercises ensure that recovery procedures remain effective.

---

## 18. Disaster Recovery

Possible failure scenarios include:

- workstation hardware failure;
- accidental deletion of files;
- disk corruption;
- operating system failure;
- Git repository corruption;
- synchronization errors;
- accidental overwriting of scientific datasets.

The combination of local backups, GitHub repositories and institutional storage minimizes the impact of these events.

---

## 19. Engineering Inventory

An engineering inventory should always be maintained.

Typical inventory items include:

- repository URL;
- active branches;
- Docker images;
- Python versions;
- operating system;
- required libraries;
- scientific datasets;
- external services;
- software licenses.

Keeping this inventory current significantly reduces recovery time after failures.

---

## 20. Recovery Checklist

Before resuming development, verify:

- repository cloned successfully;
- documentation available;
- Docker operational;
- Python environment configured;
- scientific repository synchronized;
- raster products accessible;
- application starts correctly;
- demonstration executes without errors.

Only after this checklist is complete should new development begin.


## 21. Version Compatibility

Backup files should preserve compatibility information.

Examples:

- Python version;
- Docker version;
- operating system;
- GDAL version;
- CesiumJS version;
- Dash version;
- Node.js version.

This information facilitates long-term reproducibility.

---

## 22. Engineering Snapshots

Important project milestones should generate engineering snapshots.

A snapshot typically includes:

- Git commit hash;
- documentation version;
- Docker image;
- scientific dataset version;
- demonstration screenshots;
- validation results.

Snapshots provide historical references for future comparisons.

---

## 23. Security Considerations

Backups should never expose:

- passwords;
- API keys;
- authentication tokens;
- institutional credentials;
- private certificates.

Sensitive information should remain outside the Git repository and be managed through secure configuration mechanisms.

---

## 24. Storage Recommendations

Recommended storage hierarchy:

Primary

- Developer workstation.

Secondary

- GitHub repository.

Institutional

- Microsoft Teams.

Long-term

- External archival storage.

This layered strategy reduces the probability of permanent data loss.

---

## 25. Best Practices

Always:

- commit frequently;
- synchronize GitHub regularly;
- document engineering decisions;
- verify backups periodically;
- maintain reproducible environments;
- archive major releases.

Never:

- commit passwords;
- commit temporary files;
- overwrite scientific repositories without validation;
- delete historical releases;
- ignore backup verification.

Following these practices greatly improves project reliability.


## 26. Long-Term Preservation

The Globe-CitySpace project is expected to evolve over many years.

Long-term preservation depends on:

- complete documentation;
- reproducible environments;
- version-controlled software;
- organized scientific repositories;
- validated backup procedures.

These principles ensure that future engineers can continue development independently of the original team.

---

## 27. Recovery Workflow

The complete recovery process is summarized below.

```text
Developer Workstation Failure

↓

Clone GitHub Repository

↓

Download Scientific Repository

↓

Restore Docker Environment

↓

Configure Python Environment

↓

Validate Installation

↓

Execute Demonstration

↓

Resume Development
```

Every recovery step shall follow documented engineering procedures.

---

## 28. Institutional Knowledge

The combination of:

- GitHub;
- Microsoft Teams;
- Developer Manual;
- Engineering Contracts;
- Scientific Metadata;

forms the institutional knowledge base of Globe-CitySpace.

This knowledge should remain independent of individual developers.

---

## 29. Chapter Summary

The Backup and Recovery strategy guarantees the continuity of the Globe-CitySpace project.

Its objectives are to:

- protect engineering work;
- preserve scientific datasets;
- maintain reproducible environments;
- support disaster recovery;
- facilitate onboarding of new developers;
- preserve institutional knowledge.

By combining GitHub, Microsoft Teams, local repositories and comprehensive documentation, the project can be reconstructed on a new workstation using only documented procedures.

---

# Next Chapter

**Chapter 12 — Roadmap**

---

===========================================================

END OF DOCUMENT

===========================================================