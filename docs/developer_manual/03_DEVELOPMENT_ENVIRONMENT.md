# Globe-CitySpace Engineering Handbook

---

# Chapter 03

# Development Environment

**Version:** 2.0

**Project:** Globe-CitySpace

**Institution:** Institute for Technological Research (IPT)

**Location:** São Paulo, Brazil

---

# 1. Purpose

This chapter documents the complete development environment required to build, execute and maintain the Globe-CitySpace platform.

The objective is to ensure that any future developer can recreate the same engineering environment with minimum effort.

This chapter should be considered the official installation guide for the project.

---

# 2. Development Philosophy

The Globe-CitySpace platform was developed using a reproducible engineering environment.

Every developer should work under the same software stack in order to guarantee:

- reproducible builds;
- consistent scientific processing;
- simplified maintenance;
- easier debugging;
- long-term sustainability.

---

# 3. Recommended Development Platform

The official development platform consists of:

```text
Windows 11

↓

WSL2

↓

Ubuntu 22.04 LTS

↓

Miniconda / Anaconda

↓

Python Environment

↓

Docker Desktop

↓

VS Code

↓

Git

↓

Globe-CitySpace
```

Although other environments may work, this configuration is the officially supported platform.

---

# 4. Operating System

Development is performed under Microsoft Windows using the Windows Subsystem for Linux (WSL2).

Windows is responsible for:

- desktop environment;
- browser execution;
- Docker Desktop;
- Visual Studio Code.

Linux is responsible for:

- Python execution;
- scientific processing;
- shell scripts;
- Docker commands;
- Git operations.

---

# 5. Windows Subsystem for Linux (WSL2)

WSL2 provides a native Linux environment inside Windows.

Advantages include:

- Linux compatibility;
- high performance;
- simplified package management;
- native shell scripting;
- direct integration with VS Code.

The project should always be executed inside Ubuntu rather than directly from Windows terminals.

---

# 6. Ubuntu

The official Linux distribution adopted by the project is:

Ubuntu 22.04 LTS

Ubuntu hosts:

- Python;
- Conda;
- GDAL;
- Rasterio;
- scientific libraries;
- project repository.

---

# 7. Python

Python is the primary programming language of Globe-CitySpace.

Typical responsibilities include:

- scientific processing;
- raster manipulation;
- runtime control;
- projection mapping;
- engineering automation.

The recommended version is Python 3.11 or newer.

---

# 8. Conda

Conda is used for dependency management.

Instead of installing packages globally, every scientific dependency is maintained inside an isolated environment.

This prevents version conflicts between projects.

---

# 9. Official Environment

The current project uses:

```text
geo_env_2018
```

This environment contains:

- Python
- GDAL
- Rasterio
- NumPy
- scientific dependencies
- visualization libraries

Every shell session should activate this environment before executing Globe-CitySpace.

---

# 10. Environment Activation

Typical workflow:

```bash
source ~/miniconda3/etc/profile.d/conda.sh

conda activate geo_env_2018
```

(Installation paths may differ depending on the workstation.)

---

**BLOCO 1 DE 6**

# 11. Package Management

All third-party libraries are managed through Conda and Pip.

The project avoids installing scientific packages directly into the operating system.

This approach guarantees:

- isolated environments;
- reproducible installations;
- easier upgrades;
- simplified maintenance.

Typical scientific packages include:

- GDAL
- Rasterio
- Fiona
- Shapely
- GeoPandas
- NumPy
- Pandas
- Matplotlib
- Plotly
- Dash

---

# 12. Docker

Docker is responsible for isolating application services from the operating system.

The project uses Docker primarily for:

- web services;
- runtime deployment;
- reproducible execution;
- demonstration environment.

Docker allows every developer to execute the same services independently of workstation configuration.

---

# 13. Docker Compose

Docker Compose orchestrates the project services.

Typical responsibilities include:

- container startup;
- network creation;
- volume mounting;
- service dependencies.

The standard command is:

```bash
docker compose up -d
```

Stopping all services:

```bash
docker compose down
```

---

# 14. Visual Studio Code

Visual Studio Code is the official development environment.

The recommended extensions include:

- Python
- Pylance
- Docker
- GitLens
- Markdown All in One
- YAML
- EditorConfig

VS Code should always open the repository through the WSL extension.

Never open the project using the Windows Python interpreter.

---

# 15. Repository Location

Recommended location inside WSL:

```text
/mnt/c/workspace/

        │

        ▼

ipt-cityspace-engine/

        │

        ▼

ipt_core_clean_github_clean/
```

This directory becomes the project root.

---

# 16. Git

Git is responsible for source code version control.

The repository contains:

- source code;
- documentation;
- scripts;
- configuration;
- tests.

Large scientific datasets are intentionally excluded.

---

# 17. GitHub

GitHub hosts the official software repository.

The repository stores only:

- source code;
- documentation;
- shell scripts;
- configuration;
- architecture documents.

Scientific products are maintained separately.

---

# 18. Microsoft Teams

Large scientific datasets are maintained outside GitHub.

Recommended contents include:

```text
DSM

DTM

BMP Products

CSV Products

Height Maps

Scientific Reports

Snapshots

Project Demonstrations
```

This organization prevents unnecessary repository growth.

---

# 19. Development Workflow

The recommended daily workflow is:

```text
Open Windows

↓

Start Docker Desktop

↓

Open WSL2

↓

Activate Conda

↓

Open VS Code

↓

Open Repository

↓

Develop

↓

Test

↓

Commit

↓

Push
```

---

# 20. Daily Startup Procedure

Typical startup sequence:

```bash
Open Docker Desktop

↓

Open Ubuntu

↓

conda activate geo_env_2018

↓

Open VS Code

↓

Execute start_demo2.sh

↓

Validate Services

↓

Begin Development
```

---

**BLOCO 2 DE 6**

# 21. Project Startup Scripts

To simplify daily development, the project provides startup scripts.

Typical scripts include:

```text
start_demo.sh

start_demo2.sh

run_globe_cityspace_integrated.sh

run_globe_cityspace_integrated_total.sh

start_services_docker.sh
```

These scripts automate environment initialization and reduce manual configuration.

---

# 22. Typical Startup Sequence

The recommended startup order is:

```text
1. Start Docker Desktop

↓

2. Open Ubuntu (WSL2)

↓

3. Activate geo_env_2018

↓

4. Open VS Code

↓

5. Open Repository

↓

6. Execute start_demo2.sh

↓

7. Validate URLs

↓

8. Begin Development
```

---

# 23. Typical Service URLs

During development the following services are normally available.

| Service | URL |
|----------|-----|
| Globe-CitySpace | http://localhost:8088 |
| IPT-CitySpace | http://localhost:8050 |
| Virtual Table | http://localhost:8060 |

---

# 24. Repository Organization

The GitHub repository should contain only software.

Typical contents include:

- source code;
- documentation;
- shell scripts;
- configuration files;
- Docker files;
- tests.

Large scientific products should never be committed.

---

# 25. Scientific Data Repository

Scientific datasets are maintained independently from GitHub.

Recommended organization:

```text
Microsoft Teams

│

├── DSM

├── DTM

├── Height Maps

├── BMP Products

├── CSV Products

├── Metadata

├── Scientific Reports

├── Demonstrations

└── Snapshots
```

This separation keeps the Git repository lightweight while preserving scientific reproducibility.

---

# 26. Typical Developer Workspace

```text
Windows

└── Docker Desktop

WSL2

└── Ubuntu

    └── /mnt/c/workspace/

        └── ipt-cityspace-engine/

            └── ipt_core_clean_github_clean/
```

All development activities should occur inside this workspace.

---

# 27. Recommended Daily Routine

Every development session should follow approximately this sequence.

```text
Pull latest changes

↓

Activate Conda

↓

Start Docker

↓

Run Demo

↓

Develop

↓

Test

↓

Document

↓

Commit

↓

Push
```

Maintaining a consistent routine reduces configuration errors and improves collaboration.

---

# 28. Development Best Practices

Developers are encouraged to:

- commit frequently;
- document architectural decisions;
- avoid committing generated products;
- validate changes before pushing;
- keep documentation synchronized with source code;
- preserve reproducibility.

---

# 29. Environment Validation

Before starting development, verify:

- Docker is running;
- Conda environment is active;
- repository is up to date;
- required ports are available;
- startup scripts execute successfully.

This verification prevents unnecessary debugging later.

---

# 30. Chapter Summary

The development environment combines Windows, WSL2, Ubuntu, Conda, Docker and Visual Studio Code into a reproducible engineering platform.

Using a standardized environment ensures that future developers can install, execute and maintain Globe-CitySpace with minimal configuration effort.

---

**BLOCO 3 DE 6**

# 31. Installing Windows

The recommended host operating system is Microsoft Windows 11.

Windows is responsible for:

- user interface;
- Docker Desktop;
- Visual Studio Code;
- browser execution;
- communication with WSL2.

Before starting the project, ensure that Windows Update has installed all recommended updates.

---

# 32. Installing WSL2

Install the Windows Subsystem for Linux using:

```powershell
wsl --install
```

After installation:

- reboot Windows;
- install Ubuntu 22.04 LTS;
- configure username and password.

Confirm installation:

```bash
wsl --status
```

---

# 33. Installing Ubuntu

After WSL installation:

- open Ubuntu;
- update packages;

```bash
sudo apt update

sudo apt upgrade
```

Install common development tools:

```bash
sudo apt install git

sudo apt install tree

sudo apt install curl

sudo apt install unzip

sudo apt install build-essential
```

---

# 34. Installing Miniconda

Download Miniconda for Linux.

Execute:

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

Restart Ubuntu.

Verify:

```bash
conda --version
```

---

# 35. Creating the Scientific Environment

Example:

```bash
conda create -n geo_env_2018 python=3.11
```

Activate:

```bash
conda activate geo_env_2018
```

Install project dependencies according to the project's requirements.

---

# 36. Installing Docker Desktop

Install Docker Desktop for Windows.

Enable:

- WSL2 integration;
- Ubuntu integration.

Verify:

```bash
docker version

docker compose version
```

Docker should execute correctly inside Ubuntu.

---

# 37. Installing Visual Studio Code

Install Visual Studio Code.

Recommended extensions:

- Python
- Docker
- WSL
- GitLens
- Markdown All in One
- YAML

Always open the project using:

```text
Open Folder in WSL
```

Never open the repository directly using the Windows interpreter.

---

# 38. Verifying Installation

Before developing, verify:

```bash
python --version

conda info

docker ps

git status
```

All commands should execute without errors.

---

# 39. Typical Startup Checklist

Before beginning work:

☐ Docker running

☐ Ubuntu opened

☐ Conda activated

☐ Repository updated

☐ Services started

☐ URLs responding

☐ Ready for development

---

# 40. Next Chapter

Continue with:

**Chapter 04 — Directory Structure**

---

**BLOCO 4 DE 6**

# 41. Engineering Principles

The Globe-CitySpace platform follows a set of engineering principles intended to maximize long-term maintainability.

The most important principles are:

- reproducibility;
- modularity;
- scientific traceability;
- separation of concerns;
- documentation-first development;
- version control.

Every architectural decision should preserve these principles.

---

# 42. Reproducible Environments

A new developer should be capable of recreating the complete development environment without requiring assistance from previous team members.

This objective is achieved by documenting:

- operating system;
- software versions;
- dependencies;
- installation sequence;
- directory organization;
- execution scripts.

The Engineering Handbook is the official reference for this process.

---

# 43. Dependency Management

Whenever new libraries are introduced, developers should:

- verify compatibility with existing packages;
- document installation procedures;
- update requirements files when necessary;
- test the complete pipeline.

Undocumented dependencies should never become part of the production environment.

---

# 44. Documentation Policy

Every significant software modification should update at least one of the following:

- README.md;
- Engineering Handbook;
- Architecture documentation;
- Source code comments.

Documentation must evolve together with the software.

---

# 45. Long-Term Maintenance

The project has been organized so that future developers can understand it without depending on the original authors.

For this reason, documentation explains not only **how** components work, but also **why** architectural decisions were made.

This reduces maintenance costs over the lifetime of the project.

---

# 46. Engineering Handbook

The Engineering Handbook is the primary technical reference for Globe-CitySpace.

It documents:

- architecture;
- installation;
- directory structure;
- scientific data organization;
- processing pipeline;
- Git workflow;
- backup procedures;
- recovery procedures;
- project roadmap.

Every new team member should begin by reading this manual.

---

# 47. Chapter Conclusion

The development environment presented in this chapter provides a standardized and reproducible platform for Globe-CitySpace development.

Following these recommendations ensures consistent installations, reliable scientific processing and easier collaboration among future developers.

---

=====================================

FIM DO DOCUMENTO

=====================================