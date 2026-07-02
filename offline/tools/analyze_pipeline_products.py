#!/usr/bin/env python3
"""
IPT-CitySpace
PIPELINE PRODUCT ANALYZER

Analisa os arquivos gerados no projeto para reconstruir
a sequência real do pipeline offline.

Critério:
• arquivos mais antigos → etapas iniciais
• arquivos mais recentes → etapas finais
"""

from pathlib import Path
import datetime

print("\n================================================")
print("IPT-CitySpace PIPELINE PRODUCT ANALYZER")
print("================================================\n")

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SEARCH_DIRS = [
PROJECT_ROOT / "offline/data",
PROJECT_ROOT / "offline/products"
]

files = []

print("Scanning product directories...\n")

for d in SEARCH_DIRS:

    if not d.exists():
        continue

    for f in d.rglob("*"):

        if f.is_file():

            try:

                stat = f.stat()

                files.append({
                    "path": f,
                    "time": stat.st_mtime
                })

            except Exception:
                pass

print("Files detected:", len(files))

# ------------------------------------------------
# SORT BY CREATION / MODIFICATION
# ------------------------------------------------

files_sorted = sorted(files, key=lambda x: x["time"])

print("\nPipeline reconstruction (by file generation order):\n")

for i, item in enumerate(files_sorted, start=1):

    t = datetime.datetime.fromtimestamp(item["time"])

    print(
        f"{i:03} | {t.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"{item['path'].relative_to(PROJECT_ROOT)}"
    )

print("\n================================================")
print("ANALYSIS FINISHED")
print("================================================\n")