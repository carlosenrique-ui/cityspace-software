import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("\n[FASE 3.4] Mesa virtual — leitura humana (legenda, escala, orientação)\n")

# ------------------------------------------------------------
# CAMINHOS
# ------------------------------------------------------------
FASE2_DIR = Path("products/fase2")

GRID_PATH = FASE2_DIR / "grid_uint8.npy"
MASK_PATH = FASE2_DIR / "mask_local_8x16.npy"
META_PATH = FASE2_DIR / "metadata.json"

# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------
print("[FASE 3.4] Carregando produtos da FASE 2")

grid = np.load(GRID_PATH)
mask = np.load(MASK_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

rows = meta["grid_mesa"]["rows"]
cols = meta["grid_mesa"]["cols"]
cell_cm = meta["grid_mesa"]["cell_size_cm"]

# ------------------------------------------------------------
# REDUÇÃO PARA VISUALIZAÇÃO DA MESA (8x16)
# ------------------------------------------------------------
# Usa a máscara como referência espacial
mesa = np.zeros((rows, cols), dtype=np.float32)

for r in range(rows):
    for c in range(cols):
        if mask[r, c] == 1:
            mesa[r, c] = 1.0

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
print("[FASE 3.4] Renderizando mesa com legenda")

fig, ax = plt.subplots(figsize=(10, 5))

im = ax.imshow(
    mesa,
    cmap="viridis",
    origin="lower"
)

# grid visual
ax.set_xticks(np.arange(-0.5, cols, 1))
ax.set_yticks(np.arange(-0.5, rows, 1))
ax.grid(color="white", linewidth=0.8)

# rótulos
ax.set_title("Mesa Virtual — Leitura Humana (FASE 3)")
ax.set_xlabel("Colunas da mesa (cm)")
ax.set_ylabel("Linhas da mesa (cm)")

ax.set_xticks(range(cols))
ax.set_yticks(range(rows))
ax.set_xticklabels([f"{i} cm" for i in range(cols)])
ax.set_yticklabels([f"{i} cm" for i in range(rows)])

# legenda simples
cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.04)
cbar.set_label("Presença de edifício (1 = sim)")

# anotações
ax.text(
    0.01,
    -0.15,
    f"Escala física: 1 célula = {cell_cm} cm",
    transform=ax.transAxes
)

ax.text(
    0.75,
    -0.15,
    "Norte ↑",
    transform=ax.transAxes
)

plt.tight_layout()
plt.show()

print("[FASE 3.4] Mesa com legenda exibida com sucesso\n")
