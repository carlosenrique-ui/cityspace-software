import json
import numpy as np
from pathlib import Path

print("\n[FASE C.1] Contrato temporal da mesa\n")

FASE2_DIR = Path("products/fase2")

mask = np.load(FASE2_DIR / "mask_local_8x16.npy")

with open(FASE2_DIR / "metadata.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

rows = meta["grid_mesa"]["rows"]
cols = meta["grid_mesa"]["cols"]

# ------------------------------------------------------------
# CONTRATO TEMPORAL
# ------------------------------------------------------------
time_axis = list(range(cols))

print("Contrato físico:")
print(f"  Mesa           : {cols} colunas x {rows} linhas")
print(f"  Colunas        : representam tempo discreto")
print(f"  Instantes (t)  : {time_axis}")
print("")

# ------------------------------------------------------------
# VERIFICAÇÃO CONSERVADORA
# ------------------------------------------------------------
assert mask.shape == (rows, cols), "Máscara incompatível com contrato temporal"

print("Verificações:")
print(" ✔ Máscara compatível com eixo temporal")
print(" ✔ Nenhuma modificação de dados aplicada")
print(" ✔ FASE C.1 somente interpretativa\n")

print("FASE C.1 — CONTRATO TEMPORAL DEFINIDO COM SUCESSO\n")
