import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# LOAD GRID REAL
# =========================================
df = pd.read_csv("products/final/grid_height.csv")
grid = df.pivot(index="row", columns="col", values="z_cm").values

ROWS, COLS = grid.shape

print(">>> GRID OK:", grid.shape, flush=True)

# =========================================
# LOAD ACTUATOR PLAN
# =========================================
raw = json.load(open("products/final/actuator_plan.json"))
E = raw.get("events", raw)

P = []
pos = (0, 0)

for e in E:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        P.append(pos)

print(">>> PLAN OK:", len(P), flush=True)

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
    ], style={"textAlign": "center"}),

    dcc.Interval(id="interval", interval=80),

    dcc.Store(id="t", data=0),
    dcc.Store(id="run", data=True),
    dcc.Store(id="dir", data=1)
])

# =========================================
# CONTROLES
# =========================================
@app.callback(
    Output("run","data"),
    Input("play","n_clicks"),
    Input("pause","n_clicks"),
    State("run","data"),
    prevent_initial_call=True)
def run(p, s, r):
    if ctx.triggered_id == "play":
        return True
    if ctx.triggered_id == "pause":
        return False
    return r

@app.callback(
    Output("dir","data"),
    Input("fwd","n_clicks"),
    Input("back","n_clicks"),
    State("dir","data"),
    prevent_initial_call=True)
def direction(f, b, d):
    if ctx.triggered_id == "back":
        return -1
    if ctx.triggered_id == "fwd":
        return 1
    return d

# =========================================
# TEMPO
# =========================================
@app.callback(
    Output("t","data"),
    Input("interval","n_intervals"),
    State("run","data"),
    State("dir","data"),
    State("t","data"))
def tempo(n, run, direction, t):

    if not run:
        return t

    t = t + direction

    if t >= len(P):
        t = len(P) - 1
    if t < 0:
        t = 0

    print(">>> STEP:", t, flush=True)

    return t

# =========================================
# RENDER
# =========================================
@app.callback(
    Output("g","figure"),
    Input("t","data"))
def render(step):

    Z = grid.copy()

    fig = go.Figure()

    fig.update_layout(images=[dict(
        source="assets/ipt_mask_rotated_simple.png",
        xref="x",
        yref="y",
        x=-0.5,
        y=ROWS - 0.5,
        sizex=COLS,
        sizey=ROWS,
        sizing="stretch",
        opacity=0.25,
        layer="below"
    )])

    fig.add_trace(go.Heatmap(
        z=Z,
        colorscale="Jet",
        zmin=0,
        zmax=np.max(grid),
        xgap=1,
        ygap=1
    ))

    r, c = P[step]

    fig.add_shape(
        type="rect",
        x0=c-0.5, x1=c+0.5,
        y0=r-0.5, y1=r+0.5,
        line=dict(color="white", width=4)
    )

    fig.update_layout(
        margin=dict(l=0,r=0,t=10,b=0),
        xaxis=dict(range=[-0.5, COLS-0.5], visible=False),
        yaxis=dict(range=[ROWS-0.5, -0.5], visible=False, scaleanchor="x"),
        plot_bgcolor="white"
    )

    return fig


if __name__ == "__main__":
    print(">>> V96 FIX REAL <<<", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
