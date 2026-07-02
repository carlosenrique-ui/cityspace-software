import json
import numpy as np
import pandas as pd
import dash
from dash import dcc,html,Input,Output,State
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

app=dash.Dash(__name__)

app.layout=html.Div([
 html.Div(id="status",style={"background":"black","color":"white","padding":"6px","textAlign":"center"}),
 html.Div([
  dcc.Graph(id="g",style={"width":"900px"})
 ],style={"display":"flex","justifyContent":"center"}),
 html.Div([
  html.Button("<<",id="back"),
  html.Button("Play",id="play"),
  html.Button("Pause",id="pause"),
  html.Button(">>",id="fwd")
 ],style={"textAlign":"center","marginTop":"10px"}),
 dcc.Interval(id="t",interval=120,n_intervals=0,disabled=True),
 dcc.Store(id="step",data=0),
 dcc.Store(id="run",data=False),
 dcc.Store(id="grid_state",data=np.zeros_like(grid).tolist())
])

@app.callback(Output("run","data"),
 Input("play","n_clicks"),
 Input("pause","n_clicks"),
 prevent_initial_call=True)
def run(p,pa):
 return dash.callback_context.triggered_id=="play"

@app.callback(Output("t","disabled"),
 Input("run","data"))
def toggle(run):
 return not run

@app.callback(
 Output("step","data"),
 Input("t","n_intervals"),
 Input("fwd","n_clicks"),
 Input("back","n_clicks"),
 Input("run","data"),
 Input("step","data"),
 prevent_initial_call=True)
def step(n,f,b,run,s):
 ctx=dash.callback_context.triggered_id
 if ctx=="fwd": return min((s or 0)+1,TOTAL-1)
 if ctx=="back": return max((s or 0)-1,0)
 if ctx=="t" and run: return min((s or 0)+1,TOTAL-1)
 return s

@app.callback(
 Output("g","figure"),
 Output("status","children"),
 Output("grid_state","data"),
 Input("step","data"),
 State("grid_state","data"),
 Input("run","data")
)
def render(step,grid_state,run):

 z=np.array(grid_state)

 if step<len(path):
  r,c=path[step]
  z[r][c]=values[step]

 rows,cols=z.shape

 fig=go.Figure()

 fig.add_trace(go.Heatmap(
  z=z,
  colorscale="Viridis",
  zmin=0,
  zmax=10,
  colorbar=dict(title="Altura (cm)")
 ))

 fig.update_layout(
  width=900,
  height=450,
  margin=dict(l=0,r=0,t=0,b=0)
 )

 fig.update_xaxes(scaleanchor="y",scaleratio=1,dtick=1)
 fig.update_yaxes(autorange="reversed",dtick=1)

 val=values[step] if step<len(values) else 0
 m=val/100

 status=f"STEP {step}/{TOTAL} | RUN {run} | {val:.1f} cm | {m:.2f} m"

 return fig,status,z.tolist()

app.run(debug=True,port=8050)