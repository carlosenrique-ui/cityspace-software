import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# =========================================
# LOAD CSV REAL (VALIDAÇÃO FORTE)
# =========================================
CSV_PATH = "products/final/grid_height.csv"
PLAN_PATH = "products/final/actuator_plan.json"

print(">>> LOADING CSV:", CSV_PATH, flush=True)

df = pd.read_csv(CSV_PATH)

print(">>> COLS:", df.columns.tolist(), flush=True)
print(">>> SAMPLE:", df.head(3), flush=True)

# 🔥 USA z_cm REAL
grid = df.pivot(index="row", columns="col", values="z_cm")

# GARANTE SHAPE
grid = grid.values
grid = np.flipud(grid)

ny, nx = grid.shape

print(">>> GRID SHAPE:", grid.shape, flush=True)
print(">>> GRID MAX:", np.nanmax(grid), flush=True)

# =========================================
# ESCALA REAL
# =========================================
z_cm_max = df["z_cm"].max()
z_m_max  = df["z_total_m"].max()

scale = z_m_max / z_cm_max if z_cm_max else 0

print(">>> SCALE m/cm:", scale, flush=True)

# =========================================
# LOAD PLAN REAL
# =========================================
raw = json.load(open(PLAN_PATH))
E = raw.get("events", raw)

p=[]
pos=(0,0)

for e in E:
    if e["type"]=="move":
        pos=(e["row"],e["col"])
    elif e["type"]=="set_height_cm":
        p.append(pos)

print(">>> PATH LEN:", len(p), flush=True)

# =========================================
# DASH
# =========================================
app=dash.Dash(__name__,assets_folder="assets")

app.layout=html.Div([
 dcc.Graph(id="g",config={"displayModeBar":False},style={"height":"85vh"}),
 html.Div([
  html.Button("<<",id="back"),
  html.Button("Play",id="play"),
  html.Button("Pause",id="pause"),
  html.Button(">>",id="fwd"),
 ],style={"textAlign":"center"}),
 dcc.Interval(id="interval",interval=80),
 dcc.Store(id="t",data=0),
 dcc.Store(id="run",data=False),
 dcc.Store(id="dir",data=1)
])

# =========================================
# CONTROLES
# =========================================
@app.callback(Output("run","data"),
 Input("play","n_clicks"),
 Input("pause","n_clicks"),
 State("run","data"),
 prevent_initial_call=True)
def run(a,b,c):
 return True if ctx.triggered_id=="play" else False if ctx.triggered_id=="pause" else c

@app.callback(Output("dir","data"),
 Input("fwd","n_clicks"),
 Input("back","n_clicks"),
 State("dir","data"),
 prevent_initial_call=True)
def d1(a,b,c):
 return -1 if ctx.triggered_id=="back" else 1 if ctx.triggered_id=="fwd" else c

@app.callback(Output("t","data"),
 Input("interval","n_intervals"),
 State("run","data"),
 State("dir","data"),
 State("t","data"))
def step(n,r,d,t):
 return t if not r else (t+d)%len(p)

# =========================================
# RENDER
# =========================================
@app.callback(Output("g","figure"),Input("t","data"))
def render(t):

 Z = grid.copy()

 # 🔥 FORA DO URBANISMO = INVISÍVEL
 Z[Z <= 0] = np.nan

 fig=go.Figure()

 # 🔥 IPT BASE FORTE
 fig.update_layout(images=[dict(
  source="assets/ipt_mask_rotated_simple.png",
  xref="x",yref="y",
  x=-0.5,y=ny-0.5,
  sizex=nx,sizey=ny,
  sizing="stretch",
  opacity=0.6,
  layer="below"
 )])

 ticks=np.linspace(0,10,6)
 ticktext=[f"{int(cm)} cm<br>{cm*scale:.1f} m" for cm in ticks]

 fig.add_trace(go.Heatmap(
  z=Z,
  colorscale="Viridis",
  zmin=0,
  zmax=10,
  opacity=0.35,
  xgap=1,
  ygap=1,
  colorbar=dict(title="Altura",tickvals=ticks,ticktext=ticktext)
 ))

 # 🔥 ATUADOR VISUAL
 r,c = p[t]
 fig.add_shape(
  type="rect",
  x0=c-0.5,x1=c+0.5,
  y0=r-0.5,y1=r+0.5,
  line=dict(color="white",width=3)
 )

 fig.update_layout(
  margin=dict(l=0,r=0,t=0,b=0),
  xaxis=dict(range=[-0.5,nx-0.5],visible=False),
  yaxis=dict(range=[-0.5,ny-0.5],autorange="reversed",visible=False,scaleanchor="x"),
  plot_bgcolor="white"
 )

 return fig

if __name__=="__main__":
 print(">>> V95.3 HARD OK <<<",flush=True)
 app.run(host="0.0.0.0",port=8050,debug=False)
