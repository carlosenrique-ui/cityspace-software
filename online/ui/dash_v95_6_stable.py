import json
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

print("\n==============================")
print(">>> INIT V95.6 STABLE")
print("==============================\n")

# =========================================
# LOAD GRID
# =========================================
df = pd.read_csv("products/final/grid_height.csv")

print(">>> CSV OK")

grid = df.pivot(index="row", columns="col", values="z_cm").values
grid = np.flipud(grid)

ny, nx = grid.shape

print(">>> GRID SHAPE:", grid.shape)
print(">>> MIN/MAX:", np.min(grid), np.max(grid))

# =========================================
# LOAD PLAN
# =========================================
raw = json.load(open("products/final/actuator_plan.json"))
events = raw.get("events", raw)

path = []
pos = (0,0)

for e in events:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        path.append(pos)

print(">>> PATH SIZE:", len(path))

if len(path) == 0:
    raise Exception("PATH VAZIO → offline está quebrado")

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="g"),
    dcc.Interval(id="interval", interval=300),
    dcc.Store(id="t", data=0)
])

# =========================================
# STEP (CORRIGIDO)
# =========================================
@app.callback(
    Output("t","data"),
    Input("interval","n_intervals"),
    State("t","data")
)
def step(n_intervals, t):
    if t is None:
        t = 0
    t = (t + 1) % len(path)
    print(f">>> STEP: {t}")
    return t

# =========================================
# RENDER (CORRIGIDO)
# =========================================
@app.callback(
    Output("g","figure"),
    Input("t","data")
)
def render(t):

    Z = np.full_like(grid, np.nan)

    for i in range(t + 1):
        r, c = path[i]
        Z[r, c] = grid[r, c]

    print(f">>> ACTIVE CELLS: {t+1}")
    print(f">>> CURRENT POS: {path[t]}")

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=Z,
        colorscale="Viridis",
        zmin=0,
        zmax=np.nanmax(grid),
        showscale=True,
        opacity=0.6  # 👈 transparência
    ))

    fig.update_layout(
        margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x")
    )

    return fig

# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print("\n>>> RUNNING V95.6\n")
    app.run(debug=False)
