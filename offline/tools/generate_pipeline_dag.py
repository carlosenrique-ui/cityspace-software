#!/usr/bin/env python3
"""
IPT-CitySpace
AUTO PIPELINE DAG SCANNER

Escaneia o subsistema OFFLINE e detecta dependências entre módulos.
Gera:

docs/architecture/pipeline_auto_dag.dot
docs/architecture/pipeline_auto_dag_report.txt
"""

import ast
from pathlib import Path

print("\n============================================")
print("IPT-CitySpace AUTO DAG SCANNER")
print("============================================\n")

# -------------------------------------------------
# PATHS
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OFFLINE_DIR = PROJECT_ROOT / "offline"

OUTPUT_DIR = PROJECT_ROOT / "docs" / "architecture"

DOT_FILE = OUTPUT_DIR / "pipeline_auto_dag.dot"
REPORT_FILE = OUTPUT_DIR / "pipeline_auto_dag_report.txt"

print("PROJECT ROOT:", PROJECT_ROOT)
print("OFFLINE DIR :", OFFLINE_DIR)
print("OUTPUT DIR  :", OUTPUT_DIR)

# -------------------------------------------------
# LIST PYTHON FILES
# -------------------------------------------------

print("\nScanning Python files...\n")

py_files = []

for f in OFFLINE_DIR.rglob("*.py"):

    if "__pycache__" in str(f):
        continue

    py_files.append(f)

print("Python modules found:", len(py_files))

# -------------------------------------------------
# EXTRACT IMPORTS
# -------------------------------------------------

def extract_imports(file_path):

    imports = []

    try:

        with open(file_path, "r", encoding="utf-8") as f:

            tree = ast.parse(f.read())

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for name in node.names:
                    imports.append(name.name)

            if isinstance(node, ast.ImportFrom):

                if node.module:
                    imports.append(node.module)

    except Exception:

        pass

    return imports

# -------------------------------------------------
# BUILD GRAPH
# -------------------------------------------------

print("\nBuilding dependency graph...\n")

modules = {}
edges = []

for file in py_files:

    rel = file.relative_to(PROJECT_ROOT)

    module_name = str(rel).replace("/", ".").replace(".py", "")

    imports = extract_imports(file)

    modules[module_name] = imports

for mod, imports in modules.items():

    for imp in imports:

        if imp.startswith("offline"):

            edges.append((mod, imp))

print("Modules scanned :", len(modules))
print("Dependencies    :", len(edges))

# -------------------------------------------------
# WRITE DOT FILE
# -------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\nWriting DOT graph...")

with open(DOT_FILE, "w") as f:

    f.write("digraph IPTCitySpacePipeline {\n")
    f.write("rankdir=LR;\n\n")

    for src, dst in edges:

        f.write(f'"{src}" -> "{dst}";\n')

    f.write("}\n")

print("DOT file saved:", DOT_FILE)

# -------------------------------------------------
# WRITE REPORT
# -------------------------------------------------

print("\nWriting report...")

with open(REPORT_FILE, "w") as f:

    f.write("========================================\n")
    f.write("IPT-CitySpace Pipeline Dependency Report\n")
    f.write("========================================\n\n")

    f.write("Modules scanned: " + str(len(modules)) + "\n\n")

    for src, dst in edges:

        f.write(src + " -> " + dst + "\n")

print("Report saved:", REPORT_FILE)

# -------------------------------------------------

print("\n============================================")
print("DAG GENERATION COMPLETE")
print("============================================\n")