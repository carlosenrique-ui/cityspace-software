# ============================================================
# FASE 3.1 — Mesa Virtual (Visualização 2D)
# Consome exclusivamente produtos da FASE 2
# ============================================================

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Caminhos
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]  # ipt-cityspace-engine
DATA_DIR = BASE_DIR / "products" / "fase2"

DSM_FILE = DATA_DIR / "dsm_m.npy"
DTM_FILE = DATA_DIR / "dtm_m.npy"
NDSM_FILE = DATA_DIR / "ndsm_m.npy"
GRID_FILE = DATA_DIR / "grid_uint8.npy"
META_FILE = DATA_DIR / "metadata.json"


# ------------------------------------------------------------
# Verificação defensiva
# ------------------------------------------------------------
required_files = [
    DSM_FILE,
    DTM_FILE,
    NDSM_FILE,
    GRID_FILE,
    META_FILE
]

for f in required_files:
    if not f.exists():
        raise FileNotFoundError(f"[ERRO] Arquivo não encontrado: {f}")


# ------------------------------------------------------------
# Leitura dos dados
# ------------------------------------------------------------
print("[FASE 3] Carregando produtos da FASE 2")

dsm = np.load(DSM_FILE)
dtm = np.load(DTM_FILE)
ndsm = np.load(NDSM_FILE)
grid = np.load(GRID_FILE)

with open(META_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)


# ------------------------------------------------------------
# Visualização — Mesa Virtual 2D
# ------------------------------------------------------------
print("[FASE 3] Renderizando mesa virtual")

fig, ax = plt.subplots(figsize=(10, 6))

img = ax.imshow(
    grid,
    cmap="viridis",
    origin="upper"
)

cbar = plt.colorbar(img, ax=ax)
cbar.set_label("Altura normalizada (uint8)")

ax.set_title("Mesa Virtual — FASE 3.1")
ax.set_xlabel("Eixo X (pixels da mesa)")
ax.set_ylabel("Eixo Y (pixels da mesa)")

# Norte (convencional: para cima)
ax.annotate(
    "N",
    xy=(0.95, 0.1),
    xytext=(0.95, 0.25),
    arrowprops=dict(arrowstyle="->", linewidth=2),
    ha="center",
    va="center",
    fontsize=12,
    xycoords="axes fraction"
)

# Escala textual
h, w = grid.shape
ax.text(
    0.01,
    -0.08,
    f"Resolução da mesa: {w} x {h} pixels\n"
    f"CRS: {metadata.get('crs')}",
    transform=ax.transAxes,
    fontsize=9,
    va="top"
)

plt.tight_layout()
plt.show()

print("[FASE 3] Mesa virtual exibida com sucesso")
