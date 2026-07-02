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
CSV_PATH = BASE / "offline/products/scientific/grid_metrics_utm.csv"
PNG_PATH = BASE / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png"

# =========================================
# LOAD
# =========================================

df = pd.read_csv(CSV_PATH)

z_total_cm = np.zeros((GRID_ROWS, GRID_COLS))
z_total_m = np.zeros((GRID_ROWS, GRID_COLS))

for _, r in df.iterrows():
    row = int(r["row"])
    col = int(r["col"])
    z = float(r["z_total_m"])

    if z > 0:
        z_total_m[row, col] = z
        z_total_cm[row, col] = z * 100

# NaN -> 0
z_total_cm = np.nan_to_num(z_total_cm)

# =========================================
# ZIGZAG CORRETO
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
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    dcc.Store(id="step", data=0),
    dcc.Store(id="playing", data=False),
    dcc.Store(id="direction", data=1),
    dcc.Store(id="menu-open", data=True),

    dcc.Interval(id="clock", interval=VIRTUAL_INTERVAL_MS, disabled=True),

    # MENU
    html.Div([
        html.Button("MENU", id="btn-menu"),

        html.Div(id="menu-body", children=[

            html.Label("Escala"),
            dcc.RadioItems(
                id="scale",
                options=[
                    {"label": "1x1", "value": 1},
                    {"label": "2x2", "value": 2},
                ],
                value=1
            ),

            html.Label("Mesa"),
            dcc.RadioItems(
                id="mesa",
                options=[
                    {"label": "Virtual", "value": "virtual"},
                    {"label": "Real", "value": "real"},
                ],
                value="virtual"
            ),

            html.Button("◀", id="back"),
            html.Button("⏸", id="pause"),
            html.Button("▶", id="forward"),
            html.Button("⟲", id="reset"),

        ])

    ], style={"position": "absolute", "zIndex": 10, "background": "white"}),

    dcc.Graph(id="g", style={"margin": "auto"})

])

# =========================================
# CONTROLE
# =========================================

@app.callback(
    Output("step", "data"),
    Output("playing", "data"),
    Output("direction", "data"),
    Output("clock", "disabled"),
    Output("clock", "interval"),
    Input("forward", "n_clicks"),
    Input("back", "n_clicks"),
    Input("pause", "n_clicks"),
    Input("reset", "n_clicks"),
    Input("clock", "n_intervals"),
    State("step", "data"),
    State("playing", "data"),
    State("direction", "data"),
    State("mesa", "value"),
)
def control(f, b, p, r, tick, step, playing, direction, mesa):

    trigger = ctx.triggered_id

    if trigger == "reset":
        return 0, False, 1, True, VIRTUAL_INTERVAL_MS

    if trigger == "forward":
        return step, True, 1, False, VIRTUAL_INTERVAL_MS

    if trigger == "back":
        return step, True, -1, False, VIRTUAL_INTERVAL_MS

    if trigger == "pause":
        return step, False, direction, True, VIRTUAL_INTERVAL_MS

    if trigger == "clock" and playing:
        step += direction

        if step >= TOTAL:
            step = TOTAL - 1
        if step < 0:
            step = 0

    interval = REAL_INTERVAL_MS if mesa == "real" else VIRTUAL_INTERVAL_MS

    return step, playing, direction, not playing, interval

# =========================================
# RENDER
# =========================================

@app.callback(
    Output("g", "figure"),
    Input("step", "data"),
    Input("scale", "value"),
)
def render(step, scale):

    z = np.where(z_total_cm > 0, z_total_cm, 0)

    fig = go.Figure(go.Heatmap(
        z=z,
        colorscale=[
            [0, "black"],
            [0.1, "purple"],
            [0.5, "green"],
            [1, "yellow"]
        ],
        zmin=0,
        zmax=10,
    ))

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
        xaxis_title="Av. Escola Politécnica →",
        yaxis_title="USP ↑",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    size = 16 * scale
    fig.update_layout(width=size*40, height=size*20)

    return fig


if __name__ == "__main__":
    app.run(debug=True)
