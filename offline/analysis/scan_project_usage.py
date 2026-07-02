import os
import re
from pathlib import Path

ROOT = Path(".")

# extensões relevantes
EXTENSIONS = [".py", ".json", ".md"]

# arquivos ignorados
IGNORE_DIRS = {
    "__pycache__", ".git", ".vscode",
    "backup_git", "backup_altimetry",
    "backup_scientific"
}

# =========================================
# COLETAR TODOS OS ARQUIVOS
# =========================================
all_files = []

for path in ROOT.rglob("*"):
    if path.is_file():
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix in EXTENSIONS:
            all_files.append(path)

# =========================================
# INDEXAR CONTEÚDO
# =========================================
content_map = {}

for f in all_files:
    try:
        content_map[f] = f.read_text(errors="ignore")
    except:
        content_map[f] = ""

# =========================================
# BUSCAR REFERÊNCIAS
# =========================================
used_files = set()

for f, content in content_map.items():
    for other in all_files:
        name = other.stem

        if name in content:
            used_files.add(other)

# =========================================
# CLASSIFICAÇÃO
# =========================================
unused = [f for f in all_files if f not in used_files]

# =========================================
# OUTPUT
# =========================================
print("\n==============================")
print("ARQUIVOS ATIVOS")
print("==============================\n")

for f in sorted(used_files):
    print(f)

print("\n==============================")
print("ARQUIVOS NÃO REFERENCIADOS")
print("==============================\n")

for f in sorted(unused):
    print(f)

print("\n==============================")
print(f"TOTAL: {len(all_files)}")
print(f"ATIVOS: {len(used_files)}")
print(f"NAO USADOS: {len(unused)}")
print("==============================\n")