from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# CONFIG
# =========================================

GRID_ROWS = 8
GRID_COLS = 16

VIRTUAL_INTERVAL_MS = 250
REAL_INTERVAL_MS = 1200

BASE = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BASE.parent

CSV_PATH = BASE / "offline/products/scientific/grid_metrics_utm.csv"

PNG_CANDIDATES = [
    BASE / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
    PROJECT_ROOT / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png",
]

# =========================================
# LOAD
# =========================================

def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("PNG não encontrado")

df = pd.read_csv(CSV_PATH)

Z_TOTAL_M = np.zeros((GRID_ROWS, GRID_COLS))
Z_TOTAL_CM = np.zeros((GRID_ROWS, GRID_COLS))

for _, r in df.iterrows():
    row = int(r["row"])
    col = int(r["col"])
    z = float(r["z_total_m"])

    if z > 0:
        Z_TOTAL_M[row, col] = z
        Z_TOTAL_CM[row, col] = z * 100

PNG_PATH = first_existing(PNG_CANDIDATES)
PNG = np.array(Image.open(PNG_PATH).convert("L"))

# =========================================
# ZIGZAG
# =========================================

ZIGZAG = []
for c in range(GRID_COLS - 1, -1, -1):
    if (GRID_COLS - 1 - c) % 2 == 0:
        rows = range(0, GRID_ROWS)
    else:
        rows = range(GRID_ROWS - 1, -1, -1)

    for r in rows:
        ZIGZAG.append((r, c))

TOTAL = len(ZIGZAG)

# =========================================
# FIG
# =========================================

def make_fig(step):

    fig = go.Figure()

    # 🔥 WATERMARK CORRIGIDO (não interfere no zigzag)
    fig.add_layout_image(
        dict(
            source=PNG,
            xref="x",
            yref="y",
            x=-0.5,
            y=-0.5,
            sizex=GRID_COLS,
            sizey=GRID_ROWS,
            sizing="stretch",
            opacity=0.35,
            layer="below",
        )
    )

    z = np.where(Z_TOTAL_CM > 0, Z_TOTAL_CM, 0)

    # 🔥 HEATMAP PINO (0–10 cm)
    fig.add_trace(go.Heatmap(
        z=z,
        customdata=Z_TOTAL_M,
        colorscale=[
            [0.00, "black"],
            [0.001, "black"],
            [0.02, "#440154"],
            [0.25, "#31688e"],
            [0.50, "#35b779"],
            [0.75, "#fde725"],
            [1.00, "#fde725"],
        ],
        zmin=0,
        zmax=10,
        colorbar=dict(title="Pino (cm)", x=1.02),
        hovertemplate="pino=%{z:.2f} cm<br>teto=%{customdata:.2f} m",
    ))

    # 🔥 LEGENDA TETO (0–40 m)
    fig.add_trace(go.Heatmap(
        z=[[0, 40]],
        x=[100, 101],
        y=[100, 101],
        colorscale="Viridis",
        showscale=True,
        opacity=0,
        zmin=0,
        zmax=40,
        colorbar=dict(title="Teto (m)", x=1.12),
        hoverinfo="skip"
    ))

    # 🔥 ZIGZAG
    r, c = ZIGZAG[step]

    fig.add_shape(
        type="rect",
        x0=c - 0.5,
        x1=c + 0.5,
        y0=r - 0.5,
        y1=r + 0.5,
        line=dict(color="white", width=4),
    )

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id="step", data=0),
    dcc.Interval(id="clock", interval=250, disabled=True),

    html.Button("▶", id="play"),
    html.Button("⏸", id="pause"),

    dcc.Graph(id="g")
])

@app.callback(
    Output("step", "data"),
    Output("clock", "disabled"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    Input("clock", "n_intervals"),
    State("step", "data"),
)
def run(play, pause, tick, step):

    trigger = ctx.triggered_id

    if trigger == "play":
        return step, False

    if trigger == "pause":
        return step, True

    if trigger == "clock":
        step += 1
        if step >= TOTAL:
            step = 0

    return step, True


@app.callback(
    Output("g", "figure"),
    Input("step", "data")
)
def update(step):
    return make_fig(step)


if __name__ == "__main__":
    app.run(debug=True)
