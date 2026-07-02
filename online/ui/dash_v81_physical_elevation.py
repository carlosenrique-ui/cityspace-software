import json
import numpy as np
import pandas as pd
import dash
from dash import dcc,html,Input,Output,State
import plotly.graph_objects as go

df=pd.read_csv("/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv")
grid=df.pivot(index="row",columns="col",values="z_cm").values

with open("/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json") as f:
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

timeline=[0]

for i in range(1,len(path)):
 d=dist(path[i-1],path[i])
 h=abs(values[i]-values[i-1])
 dt=0.2*d+0.08*h
 timeline.append(timeline[-1]+dt)

TMAX=timeline[-1]

app=dash.Dash(__name__)

app.layout=html.Div([
 html.Div(id="status",style={"background":"black","color":"white","padding":"6px","textAlign":"center"}),
 html.Div([dcc.Graph(id="g")],style={"display":"flex","justifyContent":"center"}),
 html.Div([
  html.Button("<<",id="back"),
  html.Button("Play",id="play"),
  html.Button("Pause",id="pause"),
  html.Button(">>",id="fwd"),
  html.Button("1x / 2x",id="zoom_btn")
 ],style={"textAlign":"center","marginTop":"10px"}),
 dcc.Interval(id="t",interval=50,n_intervals=0),
 dcc.Store(id="time",data=0),
 dcc.Store(id="run",data=False),
 dcc.Store(id="dir",data=1),
 dcc.Store(id="zoom_state",data=1)
])

@app.callback(Output("run","data"),Input("play","n_clicks"),Input("pause","n_clicks"),prevent_initial_call=True)
def run(p,pa):
 return dash.callback_context.triggered_id=="play"

@app.callback(Output("dir","data"),Input("fwd","n_clicks"),Input("back","n_clicks"),prevent_initial_call=True)
def direction(f,b):
 return -1 if dash.callback_context.triggered_id=="back" else 1

@app.callback(Output("zoom_state","data"),Input("zoom_btn","n_clicks"),State("zoom_state","data"),prevent_initial_call=True)
def zoom_toggle(n,z):
 return 2 if z==1 else 1

@app.callback(Output("time","data"),Input("t","n_intervals"),Input("run","data"),Input("dir","data"),Input("time","data"),prevent_initial_call=True)
def tick(n,run,dir,time):
 if not run:return time
 t=time+dir*0.05
 return max(0,min(TMAX,t))

def get_step(time):
 for i,t in enumerate(timeline):
  if t>=time:return i
 return len(timeline)-1

@app.callback(Output("g","figure"),Output("status","children"),Input("time","data"),Input("zoom_state","data"))
def render(time,zoom):
 step=get_step(time)
 z=np.zeros_like(grid).astype(float)
 for i,(r,c) in enumerate(path):
  if i<=step:
   if i==step:
    if i==0:
     val=values[i]
    else:
     progress=(time-timeline[i-1])/(timeline[i]-timeline[i-1])
     progress=max(0,min(1,progress))
     curve=1-(1-progress)**2
     val=values[i]*curve
   else:
    val=values[i]
   z[r][c]=val
 base_w=900
 base_h=450
 scale=2 if zoom==2 else 1
 fig=go.Figure()
 fig.add_trace(go.Heatmap(z=z,colorscale="Viridis",zmin=0,zmax=10,colorbar=dict(title="Altura (cm / m)")))
 fig.update_layout(width=base_w*scale,height=base_h*scale,margin=dict(l=0,r=0,t=0,b=0))
 fig.update_xaxes(scaleanchor="y",scaleratio=1,dtick=1,title="Colunas")
 fig.update_yaxes(autorange="reversed",dtick=1,title="Linhas")
 val=values[step] if step<len(values) else 0
 m=val/100
 status=f"STEP {step}/{TOTAL} | {val:.1f} cm | {m:.2f} m | GRID {scale}x"
 return fig,status

app.run(debug=True,port=8050)