import json
import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("\n[FASE C.2] Player temporal estático (prova de eixo X como tempo)\n")

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
grid = np.load(GRID_PATH)
mask = np.load(MASK_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

rows = meta["grid_mesa"]["rows"]
cols = meta["grid_mesa"]["cols"]

# ------------------------------------------------------------
# PREPARAÇÃO DA FIGURA
# ------------------------------------------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))

# base vazia (mesa)
base = np.zeros((rows, cols), dtype=np.float32)

im = ax.imshow(
    base,
    cmap="viridis",
    origin="lower",
    vmin=0,
    vmax=1
)

ax.set_title("FASE C.2 — Player temporal (coluna = tempo)")
ax.set_xlabel("Tempo (colunas da mesa)")
ax.set_ylabel("Linhas da mesa")

ax.set_xticks(range(cols))
ax.set_yticks(range(rows))
ax.set_xticklabels([f"t={i}" for i in range(cols)])
ax.set_yticklabels(range(rows))

ax.grid(color="white", linewidth=0.8)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# LOOP TEMPORAL ESTÁTICO
# ------------------------------------------------------------
for t in range(cols):
    print(f"[FASE C.2] Tempo t = {t}")

    frame = np.zeros((rows, cols), dtype=np.float32)

    # destaca a coluna temporal ativa
    frame[:, t] = 0.3

    # sobrepor edifícios
    frame[mask == 1] = 1.0

    im.set_data(frame)
    ax.set_title(f"FASE C.2 — Tempo t = {t}")

    plt.pause(0.8)  # pausa proposital (não é animação contínua)

print("\n[FASE C.2] Player temporal estático finalizado com sucesso\n")
plt.ioff()
plt.show()
