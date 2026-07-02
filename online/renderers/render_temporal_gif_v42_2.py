"""
IPT-CITYSPACE
Mesa Virtual — GIF Temporal V42.2

✔ Raster IPT deforma o terreno (Z)
✔ "Amassamento" contínuo (não binário)
✔ Prédios preservados
✔ Compatível NumPy 2
"""

# ============================================================
# ROOT DETECTION (BLINDADO)
# ============================================================

import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve()
while ENGINE_ROOT.name != "ipt-cityspace-engine":
    ENGINE_ROOT = ENGINE_ROOT.parent

if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

# ============================================================

import math
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from PIL import Image

from matplotlib.colors import ListedColormap, BoundaryNorm
from online.core.physical_motion_profile import generate_motion_steps

# ============================================================
# PATHS
# ============================================================

DATA_DIR = ENGINE_ROOT / "offline/products/snapshots/ipt_fase2_semantic"

GRID_PINO_CM = DATA_DIR / "grid_pino_cm.csv"
GRID_Z_TOTAL = DATA_DIR / "grid_z_total_m.csv"
RASTER_IPT = DATA_DIR / "ipt_base_raster_squashed.png"

OUT_DIR = ENGINE_ROOT / "visualization"
OUT_DIR.mkdir(parents=True, exist_ok=True)

GIF_PATH = OUT_DIR / "mesa_virtual_v42_2.gif"

# ============================================================
# PARAMETROS
# ============================================================

ALTURA_MAX_PINO_M = 0.10
DURACAO_FRAME = 0.10

# 🔥 CONTROLE DO AMASSAMENTO
Z_SQUASH_MIN = 0.15   # fora do urbanismo
Z_SQUASH_MAX = 1.0    # dentro (prédio)

# ============================================================
# COLORBREWER
# ============================================================

PAIRED_12 = [
    "#A6CEE3", "#1F78B4",
    "#B2DF8A", "#33A02C",
    "#FB9A99", "#E31A1C",
    "#FDBF6F", "#FF7F00",
    "#CAB2D6", "#6A3D9A",
    "#FFFF99", "#B15928",
]

cmap_classes = ListedColormap(PAIRED_12)
boundaries = np.linspace(0, ALTURA_MAX_PINO_M, 13)
norm_classes = BoundaryNorm(boundaries, cmap_classes.N)

# ============================================================

def load_csv(path):
    try:
        return np.loadtxt(path, delimiter=";")
    except:
        return np.loadtxt(path, delimiter=",")

def canvas_to_rgb(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    argb = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    argb = argb.reshape((h, w, 4))
    return argb[..., 1:4]

def zigzag(rows, cols):
    traj = []
    for x in range(cols):
        ys = range(rows) if x % 2 == 0 else range(rows - 1, -1, -1)
        for y in ys:
            traj.append((x, y))
    return traj

# ============================================================

def main():

    print("\n======================================")
    print("IPT-CITYSPACE — RENDER V42.2 (DEFORM)")
    print("======================================")

    grid_cm = load_csv(GRID_PINO_CM)
    grid_z = load_csv(GRID_Z_TOTAL)

    raster = np.array(Image.open(RASTER_IPT).convert("L"))

    # NumPy 2 fix
    raster = (raster - raster.min()) / (np.ptp(raster) + 1e-6)

    rows, cols = grid_cm.shape
    estado = np.zeros_like(grid_cm) / 100
    grid_m = grid_cm / 100

    traj = zigzag(rows, cols)

    print(f"[Grid] {rows}x{cols}")

    with imageio.get_writer(GIF_PATH, mode="I", duration=DURACAO_FRAME) as writer:

        for idx, (x, y) in enumerate(traj, start=1):

            base_altura = grid_m[y, x]

            # =============================
            # MAP GRID → RASTER
            # =============================
            ry = int((y / rows) * raster.shape[0])
            rx = int((x / cols) * raster.shape[1])

            r_val = raster[ry, rx]

            # =============================
            # 🔥 DEFORMAÇÃO (AMASSAMENTO)
            # =============================
            squash_factor = Z_SQUASH_MIN + r_val * (Z_SQUASH_MAX - Z_SQUASH_MIN)

            altura_deformada = base_altura * squash_factor

            estado[y, x] = altura_deformada

            fig, ax = plt.subplots(figsize=(12, 6))

            # ===== RASTER BASE =====
            ax.imshow(
                raster,
                cmap="gray",
                extent=(-0.5, cols-0.5, rows-0.5, -0.5),
                alpha=0.30,
                zorder=0
            )

            # ===== GRID DEFORMADO =====
            im = ax.imshow(
                estado,
                cmap=cmap_classes,
                norm=norm_classes,
                origin="upper",
                alpha=0.85,
                zorder=1
            )

            ax.set_title("IPT – CitySpace V42.2 (Deformação Raster)")

            ax.set_xticks([])
            ax.set_yticks([])

            frame = canvas_to_rgb(fig)
            writer.append_data(frame)
            plt.close(fig)

    print("\n[OK] GIF gerado:", GIF_PATH)


if __name__ == "__main__":
    main()