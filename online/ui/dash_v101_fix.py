# ==========================================================
# IPT-CitySpace – DASH V101 FIX (ESTÁVEL + COMPLETO)
# ==========================================================

import json
import numpy as np
from PIL import Image
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

ROWS = 8
COLS = 16

PLAN_PATH = "ipt_core_clean/products/final/actuator_plan_zigzag.json"
IPT_LOGO = "assets/ipt_mask.png"

# =========================================
# LOAD PLAN
# =========================================
with open(PLAN_PATH) as f:
    data = json.load(f)

events = data.get("events", data)

sequence = []
pos = (0, 0)

for e in events:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        h = e.get("value_cm", 0.0)
        sequence.append((pos, h))

print("SEQ LEN:", len(sequence))

# =========================================
# VELOCIDADE (RESTAURADO)
# =========================================
BASE_XY = 4
Z_SCALE = 2.5

steps = [max(BASE_XY, int(h * Z_SCALE), 1) for (_, h) in sequence]
cum = np.cumsum([0] + steps)
TOTAL = int(cum[-1])

# =========================================
# WATERMARK (GRID-ALIGNED)
# =========================================
img = Image.open(IPT_LOGO).convert("L")
img = img.resize((COLS, ROWS))
logo = np.array(img) / 255.0

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="g", config={"displayModeBar": False}, style={"height": "85vh"}),

    html.Div([
        html.Button("<<", id="back"),
        html.Button("Play", id="play"),
        html.Button("Pause", id="pause"),
        html.Button(">>", id="fwd"),
    ], style={"textAlign": "center"}),

    dcc.Interval(id="interval", interval=70),

    dcc.Store(id="t", data=0),
    dcc.Store(id="run", data=False),
    dcc.Store(id="dir", data=1)
])

# =========================================
# CONTROLES
# =========================================
@app.callback(Output("run","data"),
              Input("play","n_clicks"),
              Input("pause","n_clicks"),
              prevent_initial_call=True)
def run(p,s):
    ctx = dash.callback_context
    return "play" in ctx.triggered[0]["prop_id"]

@app.callback(Output("dir","data"),
              Input("fwd","n_clicks"),
              Input("back","n_clicks"),
              prevent_initial_call=True)
def direction(f,b):
    ctx = dash.callback_context
    return -1 if "back" in ctx.triggered[0]["prop_id"] else 1

# =========================================
# LOOP
# =========================================
@app.callback(Output("g","figure"),
              Output("t","data"),
              Input("interval","n_intervals"),
              State("t","data"),
              State("run","data"),
              State("dir","data"))
def update(n, t, run, direction):

    if run:
        t += direction

    t = max(0, min(t, TOTAL-1))

    estado = np.zeros((ROWS, COLS))

    idx = np.searchsorted(cum, t, side="right") - 1

    # preenchido
    for i in range(idx):
        (r,c),h = sequence[i]
        estado[r,c] = h

    active = None

    # atual (interpolado)
    if idx < len(sequence):
        (r,c),h = sequence[idx]

        local = t - cum[idx]
        total = steps[idx]

        frac = local/total if total > 0 else 1

        estado[r,c] = h * frac

        if idx > 0:
            (r0,c0),_ = sequence[idx-1]
        else:
            r0,c0 = r,c

        r = r0 + (r-r0)*frac
        c = c0 + (c-c0)*frac

        active = (r,c)

    # =========================================
    # WATERMARK APLICADO AO GRID
    # =========================================
    alpha = (estado > 0).astype(float)
    overlay = logo * alpha

    fig = go.Figure()

    # base
    fig.add_trace(go.Heatmap(
        z=estado,
        colorscale="Viridis",
        zmin=0,
        zmax=10,
        xgap=2,
        ygap=2
    ))

    # watermark
    fig.add_trace(go.Heatmap(
        z=overlay,
        colorscale=[
            [0, "rgba(0,0,0,0)"],
            [1, "rgba(255,255,255,0.18)"]
        ],
        showscale=False,
        xgap=2,
        ygap=2
    ))

    # cursor
    if active:
        r,c = active
        fig.add_trace(go.Scatter(
            x=[c-0.5,c+0.5,c+0.5,c-0.5,c-0.5],
            y=[r-0.5,r-0.5,r+0.5,r+0.5,r-0.5],
            mode="lines",
            line=dict(color="white", width=3),
            showlegend=False
        ))

    fig.update_layout(
        margin=dict(l=0,r=0,t=20,b=0),
        plot_bgcolor="black",
        paper_bgcolor="black"
    )

    fig.update_yaxes(autorange="reversed", scaleanchor="x", scaleratio=1)

    return fig, t

if __name__ == "__main__":
    app.run(debug=False)
