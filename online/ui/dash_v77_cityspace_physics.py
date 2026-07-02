import json
import numpy as np
import pandas as pd
import dash
from dash import dcc,html,Input,Output
import plotly.graph_objects as go

df=pd.read_csv("products/final/grid_height.csv")
grid=df.pivot(index="row",columns="col",values="z_cm").values

with open("products/final/actuator_plan.json") as f:
 raw=json.load(f)
 EVENTS=raw.get("events",raw)

path=[]
values=[]
pos=(0,0)

for e in EVENTS:
 if e["type"]=="move":
  pos=(e["row"],e["col"])
 elif e["type"]=="set_height_cm":
  path.append(pos)
  values.append(e["value_cm"])

TOTAL=len(values)

def dist(a,b):
 return abs(a[0]-b[0])+abs(a[1]-b[1])

def build_timeline():
 t=[0]
 for i in range(1,len(path)):
  d=dist(path[i-1],path[i])
  h=abs(values[i]-values[i-1])
  dt=d*0.2+h*0.05
  t.append(t[-1]+dt)
 return t

timeline=build_timeline()
TMAX=timeline[-1]

app=dash.Dash(__name__)

app.layout=html.Div([
 html.Div(id="status",style={"background":"black","color":"white","padding":"8px","textAlign":"center"}),
 dcc.Graph(id="g"),
 html.Button("Play",id="play"),
 html.Button("Pause",id="pause"),
 dcc.Interval(id="t",interval=50,n_intervals=0),
 dcc.Store(id="time",data=0),
 dcc.Store(id="run",data=False)
])

@app.callback(Output("run","data"),
 Input("play","n_clicks"),
 Input("pause","n_clicks"),
 prevent_initial_call=True)
def run(p,pa):
 return dash.callback_context.triggered_id=="play"

@app.callback(Output("time","data"),
 Input("t","n_intervals"),
 Input("run","data"),
 Input("time","data"),
 prevent_initial_call=True)
def tick(n,run,time):
 if not run: return time
 return min(time+0.1,TMAX)

def get_step(time):
 for i,t in enumerate(timeline):
  if t>=time:
   return i
 return len(timeline)-1

@app.callback(
 Output("g","figure"),
 Output("status","children"),
 Input("time","data")
)
def render(time):

 step=get_step(time)

 z=np.zeros_like(grid)

 for i,(r,c) in enumerate(path):
  if i<=step:
   z[r][c]=values[i]

 rows,cols=z.shape

 fig=go.Figure()

 fig.add_trace(go.Heatmap(
  z=z,
  colorscale="Viridis",
  zmin=0,
  zmax=10,
  colorbar=dict(title="cm / m")
 ))

 fig.update_layout(width=900,height=450,margin=dict(l=0,r=0,t=0,b=0))

 fig.update_xaxes(range=[-0.5,cols-0.5],scaleanchor="y",scaleratio=1)
 fig.update_yaxes(range=[rows-0.5,-0.5])

 val=values[step] if step<len(values) else 0
 m=val/100

 status=f"STEP {step}/{TOTAL} | RUN {True} | TIME {time:.1f}s | {val:.1f} cm | {m:.2f} m"

 return fig,status

app.run(debug=True,port=8050)