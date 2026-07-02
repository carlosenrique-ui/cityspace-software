import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

print("\n==============================")
print(">>> INIT DEBUG")
print("==============================\n")

# =========================================
# LOAD GRID
# =========================================
df = pd.read_csv("products/final/grid_height.csv")

print(">>> CSV COLS:", df.columns.tolist())
print(">>> SAMPLE:\n", df.head())

grid = df.pivot(index="row", columns="col", values="z_cm")
grid = grid.values
grid = np.flipud(grid)

ny, nx = grid.shape

print(">>> GRID SHAPE:", grid.shape)
print(">>> GRID MIN/MAX:", np.min(grid), np.max(grid))

# =========================================
# LOAD PLAN
# =========================================
raw = json.load(open("products/final/actuator_plan.json"))
E = raw.get("events", raw)

p=[]
pos=(0,0)

for e in E:
    if e["type"]=="move":
        pos=(e["row"],e["col"])
    elif e["type"]=="set_height_cm":
        p.append(pos)

print(">>> PATH SIZE:", len(p))
print(">>> FIRST 10:", p[:10])

# =========================================
# DASH
# =========================================
app=dash.Dash(__name__)

app.layout=html.Div([
 dcc.Graph(id="g",style={"height":"85vh"}),
 dcc.Interval(id="interval",interval=200),
 dcc.Store(id="t",data=0)
])

# =========================================
# STEP
# =========================================
@app.callback(Output("t","data"),
 Input("interval","n_intervals"),
 State("t","data"))
def step(n,t):
 t=(t+1)%len(p)
 print(f">>> STEP: {t}")
 return t

# =========================================
# RENDER
# =========================================
@app.callback(Output("g","figure"),Input("t","data"))
def render(t):

 Z = np.full_like(grid, np.nan)

 for i in range(t+1):
  r,c = p[i]
  Z[r,c] = grid[r,c]

 print(f">>> ACTIVE CELLS: {t+1}")
 print(f">>> CURRENT POS: {p[t]}")

 fig=go.Figure()

 fig.add_trace(go.Heatmap(
  z=Z,
  colorscale="Viridis",
  zmin=0,
  zmax=10
 ))

 fig.update_layout(
  xaxis=dict(visible=False),
  yaxis=dict(visible=False,scaleanchor="x"),
  margin=dict(l=0,r=0,t=0,b=0)
 )

 return fig

if __name__=="__main__":
 print("\n>>> RUN DEBUG\n")
 app.run(debug=False)
