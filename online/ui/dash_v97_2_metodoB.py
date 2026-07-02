# ==========================================================
# IPT-CitySpace – V97.2 MÉTODO B (TRANSFORMAÇÃO REAL)
# ==========================================================

import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

BASE = "/mnt/c/workspace/ipt-cityspace-engine"

GRID_PATH = f"{BASE}/products/final/grid_height.csv"
PLAN_PATH = f"{BASE}/products/final/actuator_plan.json"

ROWS, COLS = 8, 16

print(">>> V97.2 START", flush=True)

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

P, V = [], []
pos = None

for e in E:
    if e.get("type") == "move":
        pos = (e["row"], e["col"])
    elif e.get("type") == "set_height_cm":
        P.append(pos)
        V.append(e["value_cm"])

P, V = tuple(P), tuple(V)

N = len(P)

if N != 128:
    raise Exception("PLAN INVALIDO")

print(">>> PLAN OK (128)", flush=True)


# =========================================
# 🔥 TRANSFORMAÇÃO MÉTODO B
# =========================================
def transform(r, c):
    # origem top-left, y cresce para baixo
    rt = ROWS - 1 - r
    ct = c
    return rt, ct


# =========================================
# 🔥 TEMPO FÍSICO DISCRETO
# =========================================
BASE_DELAY = 1
HEIGHT_FACTOR = 0.3

DELAYS = [int(BASE_DELAY + HEIGHT_FACTOR * abs(v)) for v in V]


# =========================================
# ENGINE
# =========================================
def compute_state(step):
    Z = np.zeros((ROWS, COLS))

    for i in range(step + 1):
        r, c = P[i]
        rt, ct = transform(r, c)
        Z[rt][ct] = V[i]

    r, c = P[step]
    rt, ct = transform(r, c)

    return Z, (rt, ct)


# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="g", style={"height": "85vh"}),
        html.Div(
            [
                html.Button("<<", id="back"),
                html.Button("Play", id="play"),
                html.Button("Pause", id="pause"),
                html.Button(">>", id="fwd"),
            ],
            style={"textAlign": "center"},
        ),
        dcc.Interval(id="interval", interval=80),
        dcc.Store(id="step", data=0),
        dcc.Store(id="run", data=True),
        dcc.Store(id="dir", data=1),
        dcc.Store(id="tick_count", data=0),
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
# CLOCK DETERMINÍSTICO
# =========================================
@app.callback(
    Output("step", "data"),
    Output("dir", "data"),
    Output("tick_count", "data"),
    Input("interval", "n_intervals"),
    State("run", "data"),
    State("dir", "data"),
    State("step", "data"),
    State("tick_count", "data"),
)
def tick(n, run, d, step, tick_count):

    if not run:
        return step, d, tick_count

    tick_count += 1

    if tick_count < DELAYS[step]:
        return step, d, tick_count

    tick_count = 0
    step += d

    # 🔥 bounce nas bordas
    if step >= N:
        step = N - 1
        d = -1

    elif step < 0:
        step = 0
        d = 1

    return step, d, tick_count


# =========================================
# RENDER
# =========================================
@app.callback(Output("g", "figure"), Input("step", "data"))
def render(step):

    print(f">>> STEP: {step}", flush=True)

    Z, (r, c) = compute_state(step)

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=Z, colorscale="Jet", zmin=0, zmax=max(V), opacity=0.7, xgap=1, ygap=1
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

    # 🔥 NÃO usa mais inversão fake
    fig.update_yaxes(range=[-0.5, ROWS - 0.5])
    fig.update_xaxes(range=[-0.5, COLS - 0.5])

    return fig


# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print(">>> V97.2 METODO B OK <<<", flush=True)
    app.run(host="127.0.0.1", port=8050, debug=False)
