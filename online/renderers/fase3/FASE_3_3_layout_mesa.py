# ============================================================
# NOTA IMPORTANTE SOBRE ORIENTAÇÃO
#
# Este layout assume que os dados provenientes da FASE 2
# JÁ ESTÃO ROTACIONADOS no OFFLINE, conforme:
#
#   offline/geo/build_grid_fase1_1cm.py
#   ROTATION_DEG = 154.63
#
# A rotação foi aplicada UMA ÚNICA VEZ no espaço físico
# (raster + vetor), e os valores acompanham essa rotação.
#
# Portanto:
# - NÃO aplicar rotação aqui
# - NÃO alinhar com Norte geográfico
# - A mesa define o eixo X (temporal) e Y (espacial)
# ============================================================

# ============================================================
# FASE 3.3 — Layout da Mesa (Escala Física)
# ============================================================
# Responsável por declarar o contrato:
# pixel ↔ cm ↔ metro
#
# Consome exclusivamente products/fase2
# ============================================================

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Parâmetros físicos da mesa (AJUSTÁVEIS)
# ------------------------------------------------------------
MESA_LARGURA_CM = 16.0   # eixo X
MESA_ALTURA_CM = 8.0    # eixo Y


# ------------------------------------------------------------
# Caminhos
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "products" / "fase2"

GRID_FILE = DATA_DIR / "grid_uint8.npy"
NDSM_FILE = DATA_DIR / "ndsm_m.npy"
META_FILE = DATA_DIR / "metadata.json"


# ------------------------------------------------------------
# Verificação defensiva
# ------------------------------------------------------------
for f in [GRID_FILE, NDSM_FILE, META_FILE]:
    if not f.exists():
        raise FileNotFoundError(f"[ERRO] Arquivo não encontrado: {f}")


# ------------------------------------------------------------
# Leitura
# ------------------------------------------------------------
grid = np.load(GRID_FILE)
ndsm = np.load(NDSM_FILE)

with open(META_FILE, "r", encoding="utf-8") as f:
    meta = json.load(f)


# ------------------------------------------------------------
# Cálculo de escala física
# ------------------------------------------------------------
h_px, w_px = grid.shape

cm_por_pixel_x = MESA_LARGURA_CM / w_px
cm_por_pixel_y = MESA_ALTURA_CM / h_px

altura_max_m = float(ndsm.max())


print("[FASE 3.3] Contrato físico da mesa")
print(f"  Mesa física        : {MESA_LARGURA_CM} x {MESA_ALTURA_CM} cm")
print(f"  Grid (pixels)      : {w_px} x {h_px}")
print(f"  Escala X           : {cm_por_pixel_x:.4f} cm/pixel")
print(f"  Escala Y           : {cm_por_pixel_y:.4f} cm/pixel")
print(f"  Altura máx. (real) : {altura_max_m:.2f} m")


# ------------------------------------------------------------
# Visualização do layout da mesa
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))

img = ax.imshow(grid, cmap="viridis", origin="upper")

cbar = plt.colorbar(img, ax=ax)
cbar.set_label("Altura normalizada (uint8)")

ax.set_title("FASE 3.3 — Layout da Mesa (Escala Física)")
ax.set_xlabel("X (cm na mesa)")
ax.set_ylabel("Y (cm na mesa)")


# Ticks físicos
ax.set_xticks(np.linspace(0, w_px, 5))
ax.set_xticklabels(
    [f"{x:.1f}" for x in np.linspace(0, MESA_LARGURA_CM, 5)]
)

ax.set_yticks(np.linspace(0, h_px, 5))
ax.set_yticklabels(
    [f"{y:.1f}" for y in np.linspace(0, MESA_ALTURA_CM, 5)]
)


# Norte
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


# Texto técnico (contrato físico)
ax.text(
    0.01,
    -0.18,
    f"Contrato físico da mesa:\n"
    f"• {cm_por_pixel_x:.4f} cm/pixel (X)\n"
    f"• {cm_por_pixel_y:.4f} cm/pixel (Y)\n"
    f"• Altura máx. real: {altura_max_m:.2f} m\n"
    f"• CRS: {meta.get('crs')}",
    transform=ax.transAxes,
    fontsize=9,
    va="top"
)

plt.tight_layout()
plt.show()

print("[FASE 3.3] Layout da mesa exibido com sucesso")
