import json, numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

df = pd.read_csv("products/final/grid_height.csv")

grid = df.pivot(index="row", columns="col", values="z_cm").values[:8, :16]
grid = np.flipud(grid)

ny, nx = grid.shape

z_cm_max = df["z_cm"].max()
z_m_max  = df["z_total_m"].max()
scale_m_per_cm = z_m_max / z_cm_max if z_cm_max > 0 else 0

print(">>> SCALE:", scale_m_per_cm, flush=True)

raw = json.load(open("products/final/actuator_plan.json"))
E = raw.get("events", raw)

p = []
pos = (0,0)

for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)

p = [(min(r,ny-1), min(c,nx-1)) for r,c in p]

tl=[0]
d=lambda a,b:abs(a[0]-b[0])+abs(a[1]-b[1])

for i in range(1,len(p)):
    tl.append(tl[-1]+0.2*d(p[i-1],p[i]))

TMAX=tl[-1] if tl else 0

app=dash.Dash(__name__,assets_folder="assets")

app.layout=html.Div([
 dcc.Graph(id="g",config={"displayModeBar":False},style={"height":"85vh"}),
 html.Div([
  html.Button("<<",id="back"),
  html.Button("Play",id="play"),
  html.Button("Pause",id="pause"),
  html.Button(">>",id="fwd"),
 ],style={"textAlign":"center"}),
 dcc.Interval(id="interval",interval=60),
 dcc.Store(id="time",data=0),
 dcc.Store(id="run",data=False),
 dcc.Store(id="dir",data=1)
])

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

@app.callback(Output("time","data"),
 Input("interval","n_intervals"),
 State("run","data"),
 State("dir","data"),
 State("time","data"))
def t(n,r,d,t):
 return t if not r else max(0,min(TMAX,t+d*0.05))

def gs(t):
 for i,x in enumerate(tl):
  if x>=t:return i
 return len(tl)-1

@app.callback(Output("g","figure"),Input("time","data"))
def render(t):
 s=gs(t)

 Z=grid.copy()
 Z[Z==0]=np.nan

 fig=go.Figure()

 fig.update_layout(images=[dict(
  source="assets/ipt_mask_rotated_simple.png",
  xref="x",yref="y",
  x=-0.5,y=ny-0.5,
  sizex=nx,sizey=ny,
  sizing="stretch",
  opacity=0.35,
  layer="below"
 )])

 ticks=np.linspace(0,10,6)
 ticktext=[f"{int(cm)} cm<br>{cm*scale_m_per_cm:.1f} m" for cm in ticks]

 fig.add_trace(go.Heatmap(
  z=Z,
  colorscale="Jet",
  zmin=0,
  zmax=10,
  xgap=1,
  ygap=1,
  opacity=0.65,
  colorbar=dict(title="Altura",tickvals=ticks,ticktext=ticktext)
 ))

 if s<len(p):
  r,c=p[s]
  fig.add_shape(
   type="rect",
   x0=c-0.5,x1=c+0.5,
   y0=r-0.5,y1=r+0.5,
   line=dict(color="white",width=3),
   fillcolor="rgba(255,255,255,0.25)"
  )

 fig.update_layout(
  margin=dict(l=0,r=0,t=0,b=0),
  xaxis=dict(range=[-0.5,nx-0.5],visible=False),
  yaxis=dict(range=[-0.5,ny-0.5],autorange="reversed",visible=False,scaleanchor="x"),
  plot_bgcolor="white"
 )

 return fig

if __name__=="__main__":
 print(">>> V95.1 OK <<<",flush=True)
 app.run(host="0.0.0.0",port=8050,debug=False)
