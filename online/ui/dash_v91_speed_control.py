# ==========================================================
# IPT-CitySpace – DASH V91 (V84 + SPEED CONTROL)
# ==========================================================

import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

BASE = "/mnt/c/workspace/ipt-cityspace-engine"

# =========================================
# DADOS REAIS
# =========================================

df = pd.read_csv(f"{BASE}/products/final/grid_height.csv")
grid = df.pivot(index="row", columns="col", values="z_cm").values

with open(f"{BASE}/products/final/actuator_plan.json") as f:
    raw = json.load(f)

EVENTS = raw.get("events", raw)

# =========================================
# PATH REAL (ZIGZAG DO PLAN)
# =========================================

path = []
values = []
pos = (0, 0)

for e in EVENTS:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        path.append(pos)
        values.append(e["value_cm"])

TOTAL = len(values)

# =========================================
# TEMPO ORIGINAL
# =========================================

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

timeline = [0]

for i in range(1, len(path)):
    d = dist(path[i-1], path[i])
    h = abs(values[i] - values[i-1])
    dt = 0.2 * d + 0.08 * h
    timeline.append(timeline[-1] + dt)

TMAX = timeline[-1] if timeline else 0

def get_step(t):
    for i, x in enumerate(timeline):
        if x >= t:
            return i
    return len(timeline) - 1

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__, assets_folder="assets")

app.layout = html.Div([

    dcc.Graph(id="g", config={"displayModeBar": False}, style={"height": "85vh"}),

    html.Div([
        html.Button("<<", id="back"),
        html.Button("Play", id="play"),
        html.Button("Pause", id="pause"),
        html.Button(">>", id="fwd"),
        html.Button("1x", id="speed_1"),
        html.Button("5x", id="speed_5"),
        html.Button("10x", id="speed_10"),
    ], style={"textAlign": "center"}),

    dcc.Interval(id="i", interval=60),

    dcc.Store(id="t", data=0),
    dcc.Store(id="run", data=False),
    dcc.Store(id="dir", data=1),
    dcc.Store(id="speed", data=1.0)
])

# =========================================
# CONTROLES
# =========================================

@app.callback(Output("run","data"),
              Input("play","n_clicks"),
              Input("pause","n_clicks"),
              prevent_initial_call=True)
def r(a,b):
    return True if ctx.triggered_id=="play" else False

@app.callback(Output("dir","data"),
              Input("fwd","n_clicks"),
              Input("back","n_clicks"),
              prevent_initial_call=True)
def d(a,b):
    return -1 if ctx.triggered_id=="back" else 1

# =========================================
# SPEED
# =========================================

@app.callback(Output("speed","data"),
              Input("speed_1","n_clicks"),
              Input("speed_5","n_clicks"),
              Input("speed_10","n_clicks"),
              prevent_initial_call=True)
def set_speed(a,b,c):
    trig = ctx.triggered_id
    if trig == "speed_5":
        return 5.0
    elif trig == "speed_10":
        return 10.0
    return 1.0

# =========================================
# TEMPO (ÚNICA ALTERAÇÃO)
# =========================================

@app.callback(Output("t","data"),
              Input("i","n_intervals"),
              State("run","data"),
              State("dir","data"),
              State("t","data"),
              State("speed","data"))
def time(n,run,dir,t,speed):

    if not run:
        return t

    return max(0, min(TMAX, t + dir * 0.05 * speed))

# =========================================
# RENDER (V84)
# =========================================

@app.callback(Output("g","figure"), Input("t","data"))
def render(t):

    step = get_step(t)

    Z = np.zeros_like(grid)

    for i,(r,c) in enumerate(path):
        if i <= step:
            Z[r][c] = values[i]

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=Z,
        colorscale="Jet",
        zmin=0,
        zmax=10,
        xgap=0,
        ygap=0,
        opacity=0.7
    ))

    if step < len(path):
        r,c = path[step]
        fig.add_shape(type="rect",
            x0=c-0.5,y0=r-0.5,x1=c+0.5,y1=r+0.5,
            line=dict(color="white",width=2))

    ny,nx = Z.shape

    fig.update_xaxes(range=[-0.5,nx-0.5],visible=False)
    fig.update_yaxes(range=[ny-0.5,-0.5],visible=False)

    fig.update_layout(
        margin=dict(l=0,r=0,t=0,b=0),
        plot_bgcolor="black",
        paper_bgcolor="black",
        images=[dict(
            source="/assets/ipt_mask_rotated_simple.png",
            xref="paper",yref="paper",
            x=0,y=1,sizex=1,sizey=1,
            sizing="stretch",
            opacity=0.32,
            layer="below"
        )]
    )

    return fig

# =========================================
# RUN
# =========================================

print(">>> V91 SPEED CONTROL <<<")
app.run(debug=True,port=8050)
