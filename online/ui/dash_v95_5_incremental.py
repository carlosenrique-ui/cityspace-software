# ==========================================================
# IPT-CitySpace – V95.5 (INCREMENTAL ESTÁVEL)
# ==========================================================

import json, os
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

BASE = "/mnt/c/workspace/ipt-cityspace-engine"

GRID_PATH = f"{BASE}/products/final/grid_height.csv"
PLAN_PATH = f"{BASE}/products/final/actuator_plan.json"
MASK_PATH = "assets/ipt_mask_rotated_simple.png"

ROWS, COLS = 8, 16

print(">>> START V95.5", flush=True)

# =========================================
# GRID (REAL)
# =========================================
df = pd.read_csv(GRID_PATH)

grid = df.pivot(index="row", columns="col", values="z_cm").values[:ROWS, :COLS]

print(">>> GRID OK", grid.shape, flush=True)

# =========================================
# PLAN (BLINDADO)
# =========================================
raw = json.load(open(PLAN_PATH))

E = raw["events"] if isinstance(raw, dict) and "events" in raw else raw

p = []
v = []
pos = None

for e in E:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

print(">>> PLAN LEN:", len(p), flush=True)

if len(p) != 128:
    raise Exception("PLAN INVALIDO")

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__, assets_folder="assets")

app.layout = html.Div(
    [
        dcc.Graph(id="g", config={"displayModeBar": False}, style={"height": "85vh"}),
        html.Div(
            [
                html.Button("<<", id="back"),
                html.Button("Play", id="play"),
                html.Button("Pause", id="pause"),
                html.Button(">>", id="fwd"),
            ],
            style={"textAlign": "center"},
        ),
        # 🔥 MAIS LEVE (máquina fraca)
        dcc.Interval(id="interval", interval=200),
        dcc.Store(id="step", data=0),
        dcc.Store(id="run", data=True),  # 🔥 inicia automático
        dcc.Store(id="dir", data=1),
    ]
)


# =========================================
# CONTROLES
# =========================================
@app.callback(
    Output("run", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    State("run", "data"),
    prevent_initial_call=True,
)
def control_run(play, pause, current):
    if ctx.triggered_id == "play":
        return True
    elif ctx.triggered_id == "pause":
        return False
    return current


@app.callback(
    Output("dir", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("dir", "data"),
    prevent_initial_call=True,
)
def control_dir(fwd, back, current):
    if ctx.triggered_id == "fwd":
        return 1
    elif ctx.triggered_id == "back":
        return -1
    return current


# =========================================
# CLOCK (STEP ÚNICO)
# =========================================
@app.callback(
    Output("step", "data"),
    Input("interval", "n_intervals"),
    State("run", "data"),
    State("dir", "data"),
    State("step", "data"),
)
def tick(n, run, direction, step):

    if not run:
        return step

    step = step + direction

    if step < 0:
        step = 0
    if step > 127:
        step = 127

    return step


# =========================================
# RENDER
# =========================================
@app.callback(Output("g", "figure"), Input("step", "data"))
def render(step):

    print(">>> STEP:", step, flush=True)

    Z = np.zeros((ROWS, COLS))

    for i in range(step + 1):
        r, c = p[i]
        Z[r][c] = v[i]

    r, c = p[step]

    fig = go.Figure()

    # máscara IPT
    fig.update_layout(
        images=[
            dict(
                source=MASK_PATH,
                xref="x",
                yref="y",
                x=-0.5,
                y=ROWS - 0.5,
                sizex=COLS,
                sizey=ROWS,
                sizing="stretch",
                opacity=0.25,
                layer="below",
            )
        ]
    )

    fig.add_trace(
        go.Heatmap(
            z=Z, colorscale="Jet", zmin=0, zmax=max(v), opacity=0.6, xgap=1, ygap=1
        )
    )

    fig.add_shape(
        type="rect",
        x0=c - 0.5,
        x1=c + 0.5,
        y0=r - 0.5,
        y1=r + 0.5,
        line=dict(color="white", width=3),
    )

    fig.update_yaxes(range=[ROWS - 0.5, -0.5], scaleanchor="x")
    fig.update_xaxes(range=[-0.5, COLS - 0.5])

    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="white")

    return fig


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print(">>> V95.5 RUNNING <<<", flush=True)
    app.run(host="127.0.0.1", port=8050, debug=False)
