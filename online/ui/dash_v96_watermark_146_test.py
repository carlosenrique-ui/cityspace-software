import json
import base64
from io import BytesIO

import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
from PIL import Image

GRID_CSV = "/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv"
PLAN_JSON = "/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json"
WATERMARK = "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/online/assets/ipt_mask_rotated_grid_aligned_v2.png"

# ============================================================
# AJUSTE SOMENTE DO WATERMARK
# Históricos:
# máscara/geospatial: 154.63°
# pinos/grid_fit:     146.82°
# delta:               7.81°
# ============================================================
SCALE_X = 0.68
SCALE_Y = 0.60
OFFSET_X = -0.045
OFFSET_Y = -0.035
ROTATE_DEG = -7.81
WATERMARK_OPACITY = 0.30

X = (1.0 - SCALE_X) / 2.0 + OFFSET_X
Y = 1.0 - (1.0 - SCALE_Y) / 2.0 + OFFSET_Y

img = Image.open(WATERMARK).convert("RGBA")
img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
img = img.rotate(
    ROTATE_DEG,
    resample=Image.Resampling.BICUBIC,
    expand=False,
    fillcolor=(255, 255, 255, 0),
)

buf = BytesIO()
img.save(buf, format="PNG")
encoded = base64.b64encode(buf.getvalue()).decode()
IMG = f"data:image/png;base64,{encoded}"

with open(PLAN_JSON, "r", encoding="utf-8") as f:
    raw = json.load(f)

E = raw.get("events", raw)

p = []
v = []
pos = (0, 0)

for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

p = [(min(r, 7), min(c, 15)) for r, c in p]

tl = [0.0]
for i in range(1, len(p)):
    tl.append(
        tl[-1]
        + 0.2 * (abs(p[i - 1][0] - p[i][0]) + abs(p[i - 1][1] - p[i][1]))
        + 0.12 * abs(v[i])
    )

TMAX = tl[-1] if tl else 0.0
nx, ny = 16, 8

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="graph", config={"displayModeBar": False}, style={"height": "85vh"}),
        html.Div(
            [
                html.Button("<<", id="back"),
                html.Button("Play", id="play"),
                html.Button("Pause", id="pause"),
                html.Button(">>", id="fwd"),
            ],
            style={"textAlign": "center"},
        ),
        dcc.Interval(id="interval", interval=60),
        dcc.Store(id="time", data=0.0),
        dcc.Store(id="running", data=False),
        dcc.Store(id="direction", data=1),
    ]
)


@app.callback(
    Output("running", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    State("running", "data"),
    prevent_initial_call=True,
)
def cb_running(a, b, c):
    return True if ctx.triggered_id == "play" else False if ctx.triggered_id == "pause" else c


@app.callback(
    Output("direction", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("direction", "data"),
    prevent_initial_call=True,
)
def cb_direction(a, b, c):
    return -1 if ctx.triggered_id == "back" else 1 if ctx.triggered_id == "fwd" else c


@app.callback(
    Output("time", "data"),
    Input("interval", "n_intervals"),
    State("running", "data"),
    State("direction", "data"),
    State("time", "data"),
)
def cb_time(n, running, direction, t):
    return t if not running else max(0.0, min(TMAX, t + direction * 0.05))


def get_step(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


@app.callback(Output("graph", "figure"), Input("time", "data"))
def render_graph(t):
    s = get_step(t)

    Z = np.zeros((ny, nx), dtype=float)
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r, c] = v[i]

    fig = go.Figure()

    fig.update_layout(
        images=[
            dict(
                source=IMG,
                xref="paper",
                yref="paper",
                x=X,
                y=Y,
                sizex=SCALE_X,
                sizey=SCALE_Y,
                sizing="stretch",
                opacity=WATERMARK_OPACITY,
                layer="above",
            )
        ]
    )

    # HEATMAP / PINOS PRESERVADOS
    fig.add_trace(
        go.Heatmap(
            z=Z,
            colorscale="Jet",
            zmin=0,
            zmax=10,
            xgap=1,
            ygap=1,
            opacity=0.65,
            showscale=False,
        )
    )

    if s < len(p):
        r, c = p[s]
        fig.add_shape(
            type="rect",
            x0=c - 0.5,
            y0=r - 0.5,
            x1=c + 0.5,
            y1=r + 0.5,
            line=dict(color="white", width=2),
            fillcolor="rgba(255,255,255,0.25)",
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[-0.5, nx - 0.5], visible=False),
        yaxis=dict(range=[ny - 0.5, -0.5], visible=False, scaleanchor="x"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig


if __name__ == "__main__":
    print(">>> DASH V96 WATERMARK 146 TEST <<<", flush=True)
    print(f"SCALE_X={SCALE_X}", flush=True)
    print(f"SCALE_Y={SCALE_Y}", flush=True)
    print(f"OFFSET_X={OFFSET_X}", flush=True)
    print(f"OFFSET_Y={OFFSET_Y}", flush=True)
    print(f"ROTATE_DEG={ROTATE_DEG}", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
