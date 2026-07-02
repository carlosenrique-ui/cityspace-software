import json
import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("\n[FASE C.3] Player temporal com valores reais\n")

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
grid_full = np.load(GRID_PATH)
mask = np.load(MASK_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

rows = meta["grid_mesa"]["rows"]
cols = meta["grid_mesa"]["cols"]

# ------------------------------------------------------------
# AGREGAÇÃO CONSERVADORA
# ------------------------------------------------------------
# Converte o grid grande em um perfil temporal 8x16
# Estratégia conservadora: média por coluna temporal
profile = np.zeros((rows, cols), dtype=np.float32)

h, w = grid_full.shape
col_bins = np.linspace(0, w, cols + 1, dtype=int)
row_bins = np.linspace(0, h, rows + 1, dtype=int)

for r in range(rows):
    for c in range(cols):
        block = grid_full[
            row_bins[r]:row_bins[r+1],
            col_bins[c]:col_bins[c+1]
        ]
        if block.size > 0:
            profile[r, c] = block.mean()

# aplica máscara local
profile[mask == 0] = 0

# normaliza para visualização
if profile.max() > 0:
    profile = profile / profile.max()

# ------------------------------------------------------------
# VISUALIZAÇÃO
# ------------------------------------------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))

im = ax.imshow(
    profile,
    cmap="viridis",
    origin="lower",
    vmin=0,
    vmax=1
)

ax.set_title("FASE C.3 — Perfil temporal com valores")
ax.set_xlabel("Tempo (colunas da mesa)")
ax.set_ylabel("Linhas da mesa")

ax.set_xticks(range(cols))
ax.set_yticks(range(rows))
ax.set_xticklabels([f"t={i}" for i in range(cols)])
ax.set_yticklabels(range(rows))

ax.grid(color="white", linewidth=0.8)

plt.colorbar(im, ax=ax, fraction=0.025, pad=0.04, label="Valor normalizado")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# LOOP TEMPORAL
# ------------------------------------------------------------
for t in range(cols):
    print(f"[FASE C.3] Tempo t = {t}")

    frame = np.zeros_like(profile)
    frame[:, t] = profile[:, t]

    im.set_data(frame)
    ax.set_title(f"FASE C.3 — Tempo t = {t}")

    plt.pause(0.8)

print("\n[FASE C.3] Player temporal com valores finalizado\n")
plt.ioff()
plt.show()
