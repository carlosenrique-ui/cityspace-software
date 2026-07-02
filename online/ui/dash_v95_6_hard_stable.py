# ==========================================================
# IPT-CitySpace – V95.6 HARD-STABLE
# ==========================================================

import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

BASE = "/mnt/c/workspace/ipt-cityspace-engine"

GRID_PATH = f"{BASE}/products/final/grid_height.csv"
PLAN_PATH = f"{BASE}/products/final/actuator_plan.json"
MASK_PATH = "assets/ipt_mask_rotated_simple.png"

ROWS, COLS = 8, 16

print(">>> START V95.6", flush=True)

# =========================================
# GRID (REAL)
# =========================================
df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_cm").values[:ROWS, :COLS]

print(">>> GRID OK", grid.shape, flush=True)

# =========================================
# PLAN (SNAPSHOT IMUTÁVEL)
# =========================================
raw = json.load(open(PLAN_PATH))
E = raw.get("events", raw)

p = []
v = []
pos = None

for e in E:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

P = tuple(p)  # 🔒 imutável
V = tuple(v)

N = len(P)

print(">>> PLAN SIZE:", N, flush=True)

if N != 128:
    raise Exception("PLAN INVALIDO – NAO TEM 128")

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
        dcc.Interval(id="interval", interval=200),
        dcc.Store(id="step", data=0),
        dcc.Store(id="run", data=True),
        dcc.Store(id="dir", data=1),
    ]
)


# =========================================
# CONTROLES (SEM ctx = MAIS ESTÁVEL)
# =========================================
@app.callback(
    Output("run", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    State("run", "data"),
)
def run_ctrl(p_click, s_click, current):
    if p_click:
        return True
    if s_click:
        return False
    return current


@app.callback(
    Output("dir", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("dir", "data"),
)
def dir_ctrl(f_click, b_click, current):
    if f_click:
        return 1
    if b_click:
        return -1
    return current


# =========================================
# CLOCK ÚNICO (ANTI-RACE)
# =========================================
@app.callback(
    Output("step", "data"),
    Input("interval", "n_intervals"),
    State("run", "data"),
    State("dir", "data"),
    State("step", "data"),
)
def tick(n, run, d, step):

    if not run:
        return step

    step = step + d

    if step < 0:
        step = 0
    if step >= N:
        step = N - 1

    return step


# =========================================
# RENDER (BLINDADO)
# =========================================
@app.callback(Output("g", "figure"), Input("step", "data"))
def render(step):

    # 🔒 clamp definitivo
    if step < 0:
        step = 0
    if step >= N:
        step = N - 1

    print(f">>> STEP: {step}", flush=True)

    Z = np.zeros((ROWS, COLS))

    # 🔒 safe fill
    for i in range(step + 1):
        r, c = P[i]
        Z[r][c] = V[i]

    r, c = P[step]

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
            z=Z, colorscale="Jet", zmin=0, zmax=max(V), opacity=0.6, xgap=1, ygap=1
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

    return fig


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print(">>> V95.6 HARD-STABLE RUNNING <<<", flush=True)
    app.run(host="127.0.0.1", port=8050, debug=False)
