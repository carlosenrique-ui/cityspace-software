# =========================================
# IPT-CITYSPACE — DASH V112 TRUE ALIGN
# Fiel ao renderer V42, preparado para projeção na mesa real
# =========================================

from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import dash
from dash import dcc, html
import plotly.graph_objects as go

# =========================================
# PATHS
# =========================================

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    CORE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "backup_git_20260317_191244/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_v3.png",
]

# =========================================
# PROJECTION / REAL MESA PARAMETERS
# =========================================

GRID_ROWS = 8
GRID_COLS = 16

# manter igual ao V42_FINAL
OFFSET_X = 0.5
OFFSET_Y = -0.5
PNG_SCALE_X = 0.92
PNG_SCALE_Y = 0.90
PNG_OPACITY = 0.30

# modo projeção: sem título, sem toolbar, sem margens grandes
PROJECTION_MODE = True

# =========================================
# HELPERS
# =========================================

def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum PNG encontrado:\n" + "\n".join(str(p) for p in paths))


def build_grid(df):
    rows = int(df["row"].max()) + 1
    cols = int(df["col"].max()) + 1

    grid = np.zeros((rows, cols), dtype=float)

    for _, r in df.iterrows():
        grid[int(r["row"]), int(r["col"])] = float(r["z_total_m"])

    return grid


def fix_grid_like_v42(grid):
    g = grid.copy()

    # V42_FINAL: remove células fantasmas do lado esquerdo inferior
    g[6:, 0:3] = 0

    # V42_FINAL: alinhamento vertical fino
    g = np.roll(g, -1, axis=0)

    return g


def transform_png_like_v42(png_path):
    img = Image.open(png_path).convert("L")
    w, h = img.size

    img = img.resize(
        (int(w * PNG_SCALE_X), int(h * PNG_SCALE_Y)),
        Image.BICUBIC
    )

    arr = np.array(img).astype(float)

    # normalização para Plotly
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-6)

    return arr


def make_figure(grid, png):
    rows, cols = grid.shape

    fig = go.Figure()

    # =========================================
    # WATERMARK / BASE IPT
    # =========================================
    fig.add_trace(
        go.Heatmap(
            z=png,
            colorscale="Greys",
            showscale=False,
            opacity=PNG_OPACITY,
            x0=-0.5 + OFFSET_X,
            dx=(cols / png.shape[1]),
            y0=-0.5 + OFFSET_Y,
            dy=(rows / png.shape[0]),
            hoverinfo="skip",
        )
    )

    # =========================================
    # GRID z_total_m — igual V42
    # =========================================
    fig.add_trace(
        go.Heatmap(
            z=grid,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Pino / Teto<br>(m)"),
            zmin=np.nanmin(grid),
            zmax=np.nanmax(grid),
            xgap=0,
            ygap=0,
            opacity=0.85,
            hovertemplate="col=%{x}<br>row=%{y}<br>z_total=%{z:.2f} m<extra></extra>",
        )
    )

    # =========================================
    # GRID CELL BORDERS — útil para calibração da mesa real
    # =========================================
    for c in range(cols + 1):
        fig.add_trace(
            go.Scatter(
                x=[c - 0.5, c - 0.5],
                y=[-0.5, rows - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.35)", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    for r in range(rows + 1):
        fig.add_trace(
            go.Scatter(
                x=[-0.5, cols - 0.5],
                y=[r - 0.5, r - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.35)", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    title = "" if PROJECTION_MODE else "V113 — True Align FlipUD Projection Ready"

    fig.update_layout(
        title=title,
        margin=dict(l=0, r=0, t=0 if PROJECTION_MODE else 36, b=0),
        xaxis=dict(
            visible=False,
            range=[-0.5, cols - 0.5],
            constrain="domain",
        ),
        yaxis=dict(
            visible=False,
            range=[rows - 0.5, -0.5],
            scaleanchor="x",
            scaleratio=1,
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        autosize=True,
    )

    return fig


# =========================================
# LOAD
# =========================================

PNG_PATH = first_existing(PNG_CANDIDATES)

df = pd.read_csv(CSV_PATH)
grid_raw = build_grid(df)
grid = fix_grid_like_v42(grid_raw)

# =========================================
# V113 FIX — FLIP VERTICAL DO CAMPO DE CORES
# Eixo longitudinal paralelo a x'
# Mantém a máscara/raster IPT sem alteração
# =========================================
grid = np.flipud(grid)

png = transform_png_like_v42(PNG_PATH)

fig = make_figure(grid, png)

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="cityspace-v112",
            figure=fig,
            config={
                "displayModeBar": False,
                "scrollZoom": False,
                "responsive": True,
            },
            style={
                "width": "100vw",
                "height": "100vh",
            },
        )
    ],
    style={
        "margin": "0",
        "padding": "0",
        "width": "100vw",
        "height": "100vh",
        "overflow": "hidden",
        "background": "white",
    },
)

if __name__ == "__main__":
    print("========================================")
    print("V113 — TRUE ALIGN / FLIPUD / PROJECTION READY")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("Grid shape:", grid.shape)
    print("Grid min/max:", float(np.nanmin(grid)), float(np.nanmax(grid)))
    print("OFFSET_X:", OFFSET_X)
    print("OFFSET_Y:", OFFSET_Y)
    print("PNG_SCALE_X:", PNG_SCALE_X)
    print("PNG_SCALE_Y:", PNG_SCALE_Y)
    print("Projection mode:", PROJECTION_MODE)
    print("========================================")
    app.run(debug=True)
