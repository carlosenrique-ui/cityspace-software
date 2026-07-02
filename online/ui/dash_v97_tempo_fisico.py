# ==========================================================
# IPT-CitySpace – V97 TEMPO FÍSICO DOS PINOS
# ==========================================================

import json, numpy as np, pandas as pd, dash, time
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

BASE = "/mnt/c/workspace/ipt-cityspace-engine"

GRID_PATH = f"{BASE}/products/final/grid_height.csv"
PLAN_PATH = f"{BASE}/products/final/actuator_plan.json"
MASK_PATH = "assets/ipt_mask_rotated_simple.png"

ROWS, COLS = 8, 16

print(">>> V97 START", flush=True)

# =========================================
# GRID
# =========================================
df = pd.read_csv(GRID_PATH)
grid = df.pivot(index="row", columns="col", values="z_cm").values[:ROWS, :COLS]

# =========================================
# PLAN (128)
# =========================================
raw = json.load(open(PLAN_PATH))
E = raw.get("events", raw)

P = []
V = []
pos = None

for e in E:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        P.append(pos)
        V.append(e["value_cm"])

P = tuple(P)
V = tuple(V)

N = len(P)

if N != 128:
    raise Exception("PLAN INVALIDO")

print(">>> PLAN OK (128)", flush=True)

# =========================================
# 🔥 TEMPO FÍSICO
# =========================================
BASE_TIME = 0.05  # tempo mínimo
HEIGHT_FACTOR = 0.015  # impacto da altura


def compute_delay(step):
    h = abs(V[step])
    return BASE_TIME + HEIGHT_FACTOR * h


# =========================================
# ENGINE
# =========================================
def compute_state(step):
    step = max(0, min(step, N - 1))

    Z = np.zeros((ROWS, COLS))

    for i in range(step + 1):
        r, c = P[i]
        Z[r][c] = V[i]

    r, c = P[step]

    return Z, (r, c)


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
        dcc.Interval(id="interval", interval=50),
        dcc.Store(id="step", data=0),
        dcc.Store(id="run", data=True),
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
)
def run_ctrl(p, s, current):
    if p:
        return True
    if s:
        return False
    return current


@app.callback(
    Output("dir", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("dir", "data"),
)
def dir_ctrl(f, b, current):
    if f:
        return 1
    if b:
        return -1
    return current


# =========================================
# 🔥 CLOCK COM TEMPO FÍSICO
# =========================================
last_time = time.time()


@app.callback(
    Output("step", "data"),
    Output("dir", "data"),
    Input("interval", "n_intervals"),
    State("run", "data"),
    State("dir", "data"),
    State("step", "data"),
)
def tick(n, run, d, step):

    global last_time

    if not run:
        return step, d

    now = time.time()
    delay = compute_delay(step)

    if now - last_time < delay:
        return step, d

    last_time = now

    step = step + d

    # 🔥 borda com bounce
    if step >= N:
        step = N - 1
        d = -1

    elif step < 0:
        step = 0
        d = 1

    return step, d


# =========================================
# RENDER
# =========================================
@app.callback(Output("g", "figure"), Input("step", "data"))
def render(step):

    print(f">>> STEP: {step}", flush=True)

    Z, (r, c) = compute_state(step)

    fig = go.Figure()

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
    print(">>> V97 TEMPO FISICO OK <<<", flush=True)
    app.run(host="127.0.0.1", port=8050, debug=False)
