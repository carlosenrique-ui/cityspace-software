import json
import numpy as np
from pathlib import Path

print("\n[FASE 3.5] Verificação final do contrato físico e lógico\n")

FASE2_DIR = Path("products/fase2")

grid_uint8 = np.load(FASE2_DIR / "grid_uint8.npy")
mask_local = np.load(FASE2_DIR / "mask_local_8x16.npy")

with open(FASE2_DIR / "metadata.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

# ------------------------------------------------------------
# VERIFICAÇÕES
# ------------------------------------------------------------
ok = True

def check(cond, msg_ok, msg_err):
    global ok
    if cond:
        print(f"[OK] {msg_ok}")
    else:
        print(f"[ERRO] {msg_err}")
        ok = False

# Grid
check(
    grid_uint8.shape == (8, 16),
    "Grid lógico 8x16 confirmado",
    f"Grid inesperado: {grid_uint8.shape}"
)

# Máscara
check(
    mask_local.shape == (8, 16),
    "Máscara local 8x16 confirmada",
    f"Máscara inesperada: {mask_local.shape}"
)

check(
    int(mask_local.sum()) > 0,
    f"Máscara contém edifícios ({int(mask_local.sum())} células)",
    "Máscara vazia"
)

# Metadata
check(
    meta["grid_mesa"]["rows"] == 8 and meta["grid_mesa"]["cols"] == 16,
    "Metadata da mesa consistente",
    "Metadata da mesa inconsistente"
)

check(
    meta["mask_local"] is True,
    "Uso de máscara local registrado",
    "Metadata não registra máscara local"
)

# Valores
check(
    grid_uint8.max() > 0,
    f"Grid possui valores (>0): max={grid_uint8.max()}",
    "Grid sem informação"
)

print("\n--------------------------------------------------")

if ok:
    print("✔ CONTRATO FÍSICO E LÓGICO CONSOLIDADO COM SUCESSO")
else:
    print("✖ PROBLEMAS DETECTADOS — revisar antes de avançar")

print("--------------------------------------------------\n")
