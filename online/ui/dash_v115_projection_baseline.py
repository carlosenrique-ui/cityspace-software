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
# FIXED CALIBRATION — V115
# vindo do V114 calibrador
# =========================================

GRID_ROWS = 8
GRID_COLS = 16

OFFSET_X = -0.90
OFFSET_Y = -0.10
PNG_SCALE_X = 0.76
PNG_SCALE_Y = 0.60
PNG_OPACITY = 0.80

GRID_OPACITY = 0.88

# =========================================
# HELPERS
# =========================================

def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("Nenhum PNG encontrado.")


def build_grid_terrain(df):
    grid = np.full((GRID_ROWS, GRID_COLS), np.nan)

    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])
        z = float(r["z_terrain_m"])

        # regra: zero estrutural = fora / sem dado útil
        if z <= 0:
            grid[row, col] = np.nan
        else:
            grid[row, col] = z

    return grid


def fix_grid_like_v42_and_flip(grid):
    g = grid.copy()

    # remove células fantasmas do lado esquerdo inferior
    g[6:, 0:3] = np.nan

    # alinhamento vertical herdado do V42
    g = np.roll(g, -1, axis=0)

    # correção validada visualmente: flip vertical do campo
    g = np.flipud(g)

    return g


def load_png(path):
    img = Image.open(path).convert("L")
    arr = np.array(img).astype(float)
    arr = (arr - arr.min()) / (np.ptp(arr) + 1e-6)
    return arr


def make_fig(grid, png):
    rows, cols = grid.shape

    fig = go.Figure()

    # =========================================
    # WATERMARK FIXA
    # =========================================
    x_left = -0.5 + OFFSET_X
    x_right = cols - 0.5 + OFFSET_X
    y_top = -0.5 + OFFSET_Y
    y_bottom = rows - 0.5 + OFFSET_Y

    cx = (x_left + x_right) / 2
    cy = (y_top + y_bottom) / 2

    width = (x_right - x_left) * PNG_SCALE_X
    height = (y_bottom - y_top) * PNG_SCALE_Y

    x_left = cx - width / 2
    x_right = cx + width / 2
    y_top = cy - height / 2
    y_bottom = cy + height / 2

    fig.add_trace(
        go.Heatmap(
            z=png,
            x0=x_left,
            dx=(x_right - x_left) / png.shape[1],
            y0=y_top,
            dy=(y_bottom - y_top) / png.shape[0],
            colorscale="Greys",
            showscale=False,
            opacity=PNG_OPACITY,
            hoverinfo="skip",
        )
    )

    # =========================================
    # GRID z_terrain_m — BASELINE FÍSICA
    # =========================================
    fig.add_trace(
        go.Heatmap(
            z=grid,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Terreno<br>(m)"),
            zmin=np.nanmin(grid),
            zmax=np.nanmax(grid),
            opacity=GRID_OPACITY,
            xgap=0,
            ygap=0,
            hovertemplate="col=%{x}<br>row=%{y}<br>z_terrain=%{z:.2f} m<extra></extra>",
        )
    )

    # =========================================
    # LINHAS DA MESA 16x8
    # =========================================
    for c in range(cols + 1):
        fig.add_trace(
            go.Scatter(
                x=[c - 0.5, c - 0.5],
                y=[-0.5, rows - 0.5],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.45)", width=1),
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
                line=dict(color="rgba(255,255,255,0.45)", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
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
grid_raw = build_grid_terrain(df)
grid = fix_grid_like_v42_and_flip(grid_raw)
png = load_png(PNG_PATH)

fig = make_fig(grid, png)

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="cityspace-v115",
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
    print("V115 — PROJECTION BASELINE")
    print("========================================")
    print("CSV:", CSV_PATH)
    print("PNG:", PNG_PATH)
    print("Grid shape:", grid.shape)
    print("Grid terrain min/max:", float(np.nanmin(grid)), float(np.nanmax(grid)))
    print("OFFSET_X:", OFFSET_X)
    print("OFFSET_Y:", OFFSET_Y)
    print("PNG_SCALE_X:", PNG_SCALE_X)
    print("PNG_SCALE_Y:", PNG_SCALE_Y)
    print("PNG_OPACITY:", PNG_OPACITY)
    print("========================================")
    app.run(debug=True)
