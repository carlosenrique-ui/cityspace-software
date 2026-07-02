import json
import numpy as np
import pandas as pd
import dash
from dash import dcc,html,Input,Output
import plotly.graph_objects as go

print("UI LOADED")

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

app=dash.Dash(__name__)

app.layout=html.Div([
 html.H3("IPT CitySpace"),
 dcc.Graph(id="g"),
 html.Button("Play",id="play"),
 html.Button("Pause",id="pause"),
 html.Button("<<",id="back"),
 html.Button(">>",id="fwd"),
 dcc.Interval(id="t",interval=120,n_intervals=0,disabled=True),
 dcc.Store(id="s",data=0)
])

@app.callback(Output("t","disabled"),
 Input("play","n_clicks"),
 Input("pause","n_clicks"),
 prevent_initial_call=True)
def c(p,pa):
 return False if dash.callback_context.triggered_id=="play" else True

@app.callback(Output("s","data"),
 Input("t","n_intervals"),
 Input("fwd","n_clicks"),
 Input("back","n_clicks"),
 prevent_initial_call=True)
def u(n,f,b):
 ctx=dash.callback_context.triggered_id
 if ctx=="fwd": return (n or 0)+1
 if ctx=="back": return max((n or 0)-1,0)
 return n

@app.callback(Output("g","figure"),Input("s","data"))
def r(step):
 z=np.zeros_like(grid)
 for i,(rr,cc) in enumerate(path):
  if i<=step and i<len(values):
   z[rr][cc]=values[i]

 fig=go.Figure(data=go.Heatmap(
  z=z,
  colorscale="Viridis",
  zmin=0,
  zmax=10,
  showscale=True
 ))

 rows,cols=z.shape

 fig.update_layout(
  width=900,
  height=450,
  margin=dict(l=40,r=40,t=40,b=40)
 )

 fig.update_xaxes(
  range=[-0.5,cols-0.5],
  scaleanchor="y",
  scaleratio=1,
  showgrid=True,
  dtick=1
 )

 fig.update_yaxes(
  range=[rows-0.5,-0.5],
  showgrid=True,
  dtick=1
 )

 return fig

print("START DASH")
app.run(debug=True,port=8050)