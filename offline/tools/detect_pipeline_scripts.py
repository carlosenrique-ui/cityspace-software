#!/usr/bin/env python3
"""
IPT-CitySpace
PIPELINE SCRIPT DETECTOR

Escaneia o subsistema OFFLINE e detecta scripts executáveis
do pipeline científico.

Ignora automaticamente:

tests/
validation/
debug/
tools/
__pycache__/

Critério de script executável:
presença de

if __name__ == "__main__"

Resultado:
lista de scripts candidatos ao OFFLINE PIPELINE
"""

from pathlib import Path

print("\n================================================")
print("IPT-CitySpace OFFLINE PIPELINE SCRIPT DETECTOR")
print("================================================\n")

# ------------------------------------------------
# PATHS
# ------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OFFLINE_DIR = PROJECT_ROOT / "offline"

print("PROJECT ROOT :", PROJECT_ROOT)
print("OFFLINE DIR  :", OFFLINE_DIR)

# ------------------------------------------------
# IGNORE LIST
# ------------------------------------------------

IGNORE_FOLDERS = [
"tests",
"validation",
"debug",
"tools",
"__pycache__"
]

# ------------------------------------------------
# SCAN
# ------------------------------------------------

print("\nScanning OFFLINE modules...\n")

scripts = []

for file in OFFLINE_DIR.rglob("*.py"):

    skip = False

    for ignore in IGNORE_FOLDERS:

        if ignore in str(file):

            skip = True

    if skip:
        continue

    try:

        content = file.read_text()

        if 'if __name__ == "__main__"' in content:

            scripts.append(file)

    except Exception:

        pass

# ------------------------------------------------
# RESULT
# ------------------------------------------------

scripts = sorted(scripts)

print("Executable pipeline scripts detected:", len(scripts))
print()

for s in scripts:

    print(" •", s.relative_to(PROJECT_ROOT))

print("\n================================================")
print("SCAN FINISHED")
print("================================================\n")