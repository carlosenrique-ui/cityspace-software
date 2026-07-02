# ============================================================
# FASE C.4.1 — Renderer Canônico da Mesa (com referências reais)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

# -------------------------------
# CONFIGURAÇÕES DA MESA
# -------------------------------
ROWS = 8
COLS = 16
CELL_SIZE_CM = 1.0   # mesa manda
ROTATION_DEG = 154.63  # rotação real do IPT (referência)

# Escala equivalente (exemplo conservador)
# (ajuste depois se quiser refinar)
CM_TO_METERS_EQUIV = 12.0  # 1 cm ≈ 12 m (informativo)

# -------------------------------
# DADOS DE EXEMPLO (TEMPORAL)
# -------------------------------
# Simula um estado acumulado (subida progressiva)
grid = np.zeros((ROWS, COLS), dtype=float)
for t in range(COLS):
    grid[:, t] = np.linspace(0, 1, ROWS) * (t / (COLS - 1))

# -------------------------------
# PLOT BASE
# -------------------------------
fig, ax = plt.subplots(figsize=(10, 5))

im = ax.imshow(
    grid,
    cmap="plasma",
    origin="upper",
    vmin=0,
    vmax=1
)

# -------------------------------
# EIXOS HONESTOS (MESA)
# -------------------------------
ax.set_xticks(range(COLS))
ax.set_yticks(range(ROWS))

ax.set_xlabel("Colunas da mesa (X / tempo discreto)")
ax.set_ylabel("Linhas da mesa (Y)")

ax.set_title(
    "Mesa Virtual Canônica 8×16 — Estado Temporal\n"
    "Sistema local da mesa (referências cartográficas auxiliares)",
    fontsize=11
)

# -------------------------------
# CURSOR TEMPORAL (quadrado branco)
# -------------------------------
t_cursor = 5
cursor = Rectangle(
    (t_cursor - 0.5, -0.5),
    1, ROWS,
    linewidth=2,
    edgecolor="white",
    facecolor="none"
)
ax.add_patch(cursor)

# -------------------------------
# BARRA DE ESCALA (MESA)
# -------------------------------
scale_x = 0.5
scale_y = ROWS + 0.3

ax.text(scale_x, scale_y, "Escala da mesa:", fontsize=9, ha="left", va="center")

ax.add_patch(Rectangle((scale_x, scale_y + 0.1), 1, 0.2, color="white"))
ax.text(scale_x + 0.5, scale_y + 0.45, "1 cm", ha="center", fontsize=8)

ax.add_patch(Rectangle((scale_x + 1.2, scale_y + 0.1), 2, 0.2, color="white"))
ax.text(scale_x + 2.2, scale_y + 0.45, "2 cm", ha="center", fontsize=8)

ax.text(
    scale_x,
    scale_y + 0.8,
    f"Equivalência aprox.: 1 cm ≈ {CM_TO_METERS_EQUIV:.0f} m",
    fontsize=8,
    ha="left"
)

# -------------------------------
# ROSA DOS VENTOS (AUXILIAR)
# -------------------------------
arrow = FancyArrowPatch(
    (COLS - 2, ROWS - 1),
    (COLS - 2, ROWS - 3),
    arrowstyle="->",
    color="white",
    linewidth=2
)
ax.add_patch(arrow)

ax.text(
    COLS - 2,
    ROWS - 3.3,
    "N",
    color="white",
    ha="center",
    va="bottom",
    fontsize=10
)

ax.text(
    COLS - 3.8,
    ROWS - 0.5,
    f"Norte geográfico (ref.)\nMesa rotacionada +{ROTATION_DEG:.2f}°",
    fontsize=7,
    ha="left",
    va="top"
)

# -------------------------------
# COLORBAR
# -------------------------------
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Altura normalizada do pino (referência visual)")

plt.tight_layout()
plt.show()

print("[FASE C.4.1] Renderer canônico exibido com sucesso")
