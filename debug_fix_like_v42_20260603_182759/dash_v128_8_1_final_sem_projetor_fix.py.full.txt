from pathlib import Path
import base64
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

from scipy.ndimage import zoom, gaussian_filter
import matplotlib.pyplot as plt


# =========================================
# PATHS / CONFIG
# =========================================

THIS_FILE = Path(__file__).resolve()
CORE_ROOT = THIS_FILE.parents[2]
PROJECT_ROOT = CORE_ROOT.parent

CSV_PATH = CORE_ROOT / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    CORE_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
]

NORTH_CANDIDATES = [
    CORE_ROOT / "online/assets/north_arrow_scale.png",
    PROJECT_ROOT / "online/assets/north_arrow_scale.png",
]

GRID_ROWS = 8
GRID_COLS = 16

OFFSET_X = -0.90
OFFSET_Y = -0.10
PNG_SCALE_X = 0.76
PNG_SCALE_Y = 0.60

PNG_OPACITY = 0.80
GRID_OPACITY = 0.88

VIRTUAL_INTERVAL_MS = 250


# =========================================
# LOADERS
# =========================================

def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def image_to_data_uri(path):
    if path is None:
        return None
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"


def fix_like_v42(grid):
    g = grid.copy()
    g = np.roll(g, -1, axis=0)
    g = np.flipud(g)
    return g


def build_grids(df):
    z_total_m = np.full((GRID_ROWS, GRID_COLS), np.nan)

    for _, r in df.iterrows():
        row = int(r["row"])
        col = int(r["col"])
        total = float(r["z_total_m"])

        if total > 0:
            z_total_m[row, col] = total

    return fix_like_v42(z_total_m)


# =========================================
# ZIGZAG
# =========================================

def build_zigzag_path():
    path = []
    for c in range(GRID_COLS):
        if c % 2 == 0:
            rows = range(GRID_ROWS)
        else:
            rows = range(GRID_ROWS - 1, -1, -1)

        for r in rows:
            path.append((r, c))

    return path


# =========================================
# DRAW HELPERS
# =========================================

def add_watermark(fig):
    fig.add_layout_image(dict(
        source=PNG_URI,
        xref="x",
        yref="y",
        x=-0.5,
        y=-0.5,
        sizex=GRID_COLS,
        sizey=GRID_ROWS,
        opacity=0.25,
        layer="below"
    ))


def add_north(fig):
    if NORTH_URI:
        fig.add_layout_image(dict(
            source=NORTH_URI,
            xref="paper",
            yref="paper",
            x=-0.05,
            y=0.02,
            sizex=0.25,
            sizey=0.25,
            layer="above"
        ))


def add_annotations(fig):
    fig.add_annotation(
        x=-1.2,
        y=GRID_ROWS / 2,
        text="USP",
        textangle=-90,
        showarrow=False,
        font=dict(size=18)
    )

    fig.add_annotation(
        x=GRID_COLS / 2,
        y=GRID_ROWS + 0.8,
        text="Av. Escola Politécnica",
        showarrow=False,
        font=dict(size=18)
    )


def active_cell(row, col):
    return dict(
        type="rect",
        x0=col - 0.5,
        x1=col + 0.5,
        y0=row - 0.5,
        y1=row + 0.5,
        line=dict(color="white", width=3)
    )


def make_fig(step):
    fig = go.Figure()

    if PNG_URI:
        add_watermark(fig)

    z = np.nan_to_num(Z_TOTAL_M)

    fig.add_trace(go.Heatmap(
        z=z,
        colorscale="Viridis",
        showscale=True
    ))

    row, col = ZIGZAG_PATH[step]

    fig.update_layout(
        shapes=[active_cell(row, col)],
        xaxis=dict(range=[-0.5, GRID_COLS - 0.5], visible=False),
        yaxis=dict(range=[GRID_ROWS - 0.5, -0.5], visible=False),
        margin=dict(l=120, r=40, t=80, b=40),
        plot_bgcolor="white"
    )

    add_annotations(fig)
    add_north(fig)

    return fig


# =========================================
# LOAD DATA
# =========================================

PNG_PATH = first_existing(PNG_CANDIDATES)
NORTH_PATH = first_existing(NORTH_CANDIDATES)

PNG_URI = image_to_data_uri(PNG_PATH)
NORTH_URI = image_to_data_uri(NORTH_PATH)

DF = pd.read_csv(CSV_PATH)
Z_TOTAL_M = build_grids(DF)

ZIGZAG_PATH = build_zigzag_path()
TOTAL_STEPS = len(ZIGZAG_PATH)


# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id="clock", interval=VIRTUAL_INTERVAL_MS),

    html.Button("◀ Backward", id="back"),
    html.Button("▶ Forward", id="forward"),

    dcc.Graph(id="graph")
])


# =========================================
# CALLBACK
# =========================================

@app.callback(
    Output("graph", "figure"),
    Input("clock", "n_intervals")
)
def update(n):
    step = n % TOTAL_STEPS
    return make_fig(step)


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)
