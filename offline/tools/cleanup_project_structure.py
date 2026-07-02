"""
IPT-CitySpace
Architectural Cleanup Script

Objetivo
--------

Organizar o projeto movendo scripts legados
para a pasta legacy automaticamente.

Este script:

1) cria pasta legacy com timestamp
2) move código antigo
3) preserva pipeline científico
4) executa git commit automático
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


print("\n==========================================")
print("IPT-CitySpace PROJECT ARCHITECTURE CLEANUP")
print("==========================================\n")


BASE = Path(__file__).resolve().parents[2]
LEGACY_ROOT = BASE / "legacy"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LEGACY_DIR = LEGACY_ROOT / f"cleanup_{timestamp}"

print("BASE PROJECT:")
print(BASE)

print("\nCreating legacy directory:")
print(LEGACY_DIR)

LEGACY_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# LISTA DE DIRETÓRIOS LEGADOS
# --------------------------------------------------

legacy_dirs = [

    "offline/geo",
    "offline/exporting",
]

# --------------------------------------------------
# LISTA DE ARQUIVOS LEGADOS
# --------------------------------------------------

legacy_files = [

    "offline/debug_extents.py",
    "arquivo.py"
]

# --------------------------------------------------
# MOVER DIRETÓRIOS
# --------------------------------------------------

print("\nMoving legacy directories...\n")

moved_anything = False

for rel in legacy_dirs:

    src = BASE / rel

    if src.exists():

        dst = LEGACY_DIR / src.name

        print("Moving directory:")
        print(src)
        print(" -> ")
        print(dst)
        print()

        shutil.move(str(src), str(dst))

        moved_anything = True

    else:

        print("Directory not found (skip):", src)


# --------------------------------------------------
# MOVER ARQUIVOS
# --------------------------------------------------

print("\nMoving legacy files...\n")

for rel in legacy_files:

    src = BASE / rel

    if src.exists():

        dst = LEGACY_DIR / src.name

        print("Moving file:")
        print(src)
        print(" -> ")
        print(dst)
        print()

        shutil.move(str(src), str(dst))

        moved_anything = True

    else:

        print("File not found (skip):", src)


# --------------------------------------------------
# GIT COMMIT
# --------------------------------------------------

print("\n====================================")
print("Running Git commit")
print("====================================\n")

if moved_anything:

    subprocess.run(["git", "add", "."])

    msg = f"architecture cleanup – legacy migration {timestamp}"

    subprocess.run(["git", "commit", "-m", msg])

    print("\nGit commit completed.")

else:

    print("Nothing moved. Git commit skipped.")


print("\n====================================")
print("PROJECT CLEANUP FINISHED")
print("====================================\n")