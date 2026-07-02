# ==========================================================
# IPT-CitySpace – DASH V96 (ROTATION 90° CLOCKWISE CORRETA)
# ==========================================================

import json
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# =========================================
# CONFIG
# =========================================
ROWS = 8
COLS = 16

PLAN_PATH = "ipt_core_clean/products/final/actuator_plan.json"
MASK_PATH = "assets/ipt_mask.png"

# =========================================
# LOAD PLAN
# =========================================
with open(PLAN_PATH) as f:
    data = json.load(f)

events = data.get("events", data)

sequence = []
pos = (0,0)

for e in events:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        h = (
            e.get("value_cm")
            or e.get("height_cm")
            or e.get("cm")
            or e.get("value")
            or 0.0
        )
        sequence.append((pos, h))

print(">>> SEQ LEN:", len(sequence))

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="g", style={"height":"85vh"}),

    html.Div([
        html.Button("<<", id="back"),
        html.Button("Play", id="play"),
        html.Button("Pause", id="pause"),
        html.Button(">>", id="fwd"),
    ], style={"textAlign":"center"}),

    dcc.Interval(id="interval", interval=200),

    dcc.Store(id="idx", data=0),
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
    if "play" in ctx.triggered[0]["prop_id"]:
        return True
    return False


@app.callback(Output("dir","data"),
              Input("fwd","n_clicks"),
              Input("back","n_clicks"),
              prevent_initial_call=True)
def direction(f,b):
    ctx = dash.callback_context
    if "back" in ctx.triggered[0]["prop_id"]:
        return -1
    return 1


# =========================================
# LOOP PRINCIPAL
# =========================================
@app.callback(
    Output("g","figure"),
    Output("idx","data"),
    Input("interval","n_intervals"),
    State("idx","data"),
    State("run","data"),
    State("dir","data")
)
def update(n, idx, run, direction):

    if run:
        idx += direction

    idx = max(0, min(idx, len(sequence)-1))

    # 🔥 MATRIZ ROTACIONADA
    estado = np.zeros((COLS, ROWS))  # (16 x 8)

    for i in range(idx+1):
        (r, c), h = sequence[i]

        # =========================================
        # 🔥 TRANSFORMAÇÃO CORRETA (90° CLOCKWISE)
        # =========================================
        r_plot = c
        c_plot = ROWS - 1 - r

        estado[r_plot, c_plot] = h

    fig = go.Figure()

    # =========================================
    # IPT MASK (SE EXISTIR)
    # =========================================
    try:
        ipt_mask = plt.imread(MASK_PATH)

        fig.add_layout_image(
            dict(
                source=ipt_mask,
                x=0,
                y=COLS,
                sizex=COLS,
                sizey=ROWS,
                xref="x",
                yref="y",
                opacity=0.25,
                layer="below"
            )
        )
    except:
        pass

    fig.add_trace(go.Heatmap(
        z=estado,
        colorscale="Viridis"
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0)
    )

    return fig, idx


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    app.run(debug=False)

