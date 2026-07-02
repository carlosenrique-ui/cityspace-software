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
# CONFIG
# =========================================

GRID_ROWS = 8
GRID_COLS = 16

BASE = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BASE.parent

CSV_PATH = BASE / "offline/products/scientific/grid_metrics_utm.csv"

PNG_PATH = BASE / "offline/products/snapshots/ipt_fase2_semantic/ipt_base_raster_aligned_final.png"

NORTH_PATH = BASE / "online/assets/north_arrow_scale.png"

TETO_MAX_M = 40.0
PINO_MAX_CM = 10.0


# =========================================
# LOAD
# =========================================

df = pd.read_csv(CSV_PATH)

Z_TOTAL_M = np.full((GRID_ROWS, GRID_COLS), np.nan)

for _, r in df.iterrows():
    row = int(r["row"])
    col = int(r["col"])
    z = float(r["z_total_m"])

    if z > 0:
        Z_TOTAL_M[row, col] = z

Z_PINO_CM = (Z_TOTAL_M / TETO_MAX_M) * PINO_MAX_CM
Z_PINO_CM = np.clip(Z_PINO_CM, 0, PINO_MAX_CM)


# =========================================
# IMAGE UTILS
# =========================================

def to_uri(path):
    if not Path(path).exists():
        return None
    b = Path(path).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode()

PNG_URI = to_uri(PNG_PATH)
NORTH_URI = to_uri(NORTH_PATH)


# =========================================
# ZIGZAG (CORRETO)
# =========================================

ZIGZAG = []
for c in range(GRID_COLS):
    if c % 2 == 0:
        rows = range(GRID_ROWS)
    else:
        rows = range(GRID_ROWS - 1, -1, -1)

    for r in rows:
        ZIGZAG.append((r, c))

TOTAL = len(ZIGZAG)


# =========================================
# GRID PROGRESSIVO
# =========================================

def build_progress(step):
    z = np.zeros_like(Z_PINO_CM)

    for i in range(step + 1):
        r, c = ZIGZAG[i]
        if np.isfinite(Z_PINO_CM[r, c]):
            z[r, c] = Z_PINO_CM[r, c]

    return z


# =========================================
# FIGURE
# =========================================

def make_fig(step):

    fig = go.Figure()

    # watermark
    if PNG_URI:
        fig.add_layout_image(dict(
            source=PNG_URI,
            xref="x",
            yref="y",
            x=-0.5,
            y=-0.5,
            sizex=GRID_COLS,
            sizey=GRID_ROWS,
            sizing="stretch",
            opacity=0.35,
            layer="below"
        ))

    z = build_progress(step)

    fig.add_trace(go.Heatmap(
        z=z,
        customdata=Z_TOTAL_M,
        colorscale=[
            [0.00, "black"],
            [0.001, "black"],
            [0.25, "#31688e"],
            [0.50, "#35b779"],
            [0.75, "#fde725"],
            [1.00, "#fde725"],
        ],
        zmin=0,
        zmax=10,
        colorbar=dict(
            title="Pino(cm) / Teto(m)",
            tickvals=[0,2.5,5,7.5,10],
            ticktext=["0/0","2.5/10","5/20","7.5/30","10/40"]
        ),
        hovertemplate="pino=%{z:.2f}cm<br>teto=%{customdata:.2f}m"
    ))

    r, c = ZIGZAG[step]

    fig.add_shape(
        type="rect",
        x0=c-0.5, x1=c+0.5,
        y0=r-0.5, y1=r+0.5,
        line=dict(color="white", width=4)
    )

    # título
    fig.add_annotation(
        x=7.5, y=8.6,
        text="<b>CitySpace</b>",
        showarrow=False,
        font=dict(size=24)
    )

    # eixo X
    fig.add_annotation(
        x=7.5, y=-1.2,
        text="Av. Escola Politécnica →",
        showarrow=False,
        font=dict(size=18)
    )

    # eixo Y
    fig.add_annotation(
        x=-1.5, y=3.5,
        text="USP",
        textangle=-90,
        showarrow=False,
        font=dict(size=18)
    )

    # north scale
    if NORTH_URI:
        fig.add_layout_image(dict(
            source=NORTH_URI,
            xref="paper",
            yref="paper",
            x=0.02,
            y=0.02,
            sizex=0.25,
            sizey=0.25,
            layer="above"
        ))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-0.5, GRID_COLS-0.5]),
        yaxis=dict(visible=False, range=[GRID_ROWS-0.5, -0.5], scaleanchor="x"),
        margin=dict(l=40,r=40,t=40,b=40),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig


# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    dcc.Store(id="step", data=0),
    dcc.Interval(id="clock", interval=250, disabled=True),

    html.Button("◀ Backward", id="back"),
    html.Button("⏸ Pause", id="pause"),
    html.Button("▶ Forward", id="forward"),

    dcc.Graph(id="g")

])


@app.callback(
    Output("step","data"),
    Output("clock","disabled"),
    Input("forward","n_clicks"),
    Input("back","n_clicks"),
    Input("pause","n_clicks"),
    Input("clock","n_intervals"),
    State("step","data")
)
def control(f,b,p,tick,step):

    trig = ctx.triggered_id

    if trig == "forward":
        step = min(step+1, TOTAL-1)
        return step, False

    if trig == "back":
        step = max(step-1, 0)
        return step, False

    if trig == "pause":
        return step, True

    if trig == "clock":
        step += 1
        if step >= TOTAL:
            step = TOTAL-1
        return step, False

    return step, True


@app.callback(
    Output("g","figure"),
    Input("step","data")
)
def update(step):
    return make_fig(step)


if __name__ == "__main__":
    print("V128.8 OK")
    app.run(debug=True)

