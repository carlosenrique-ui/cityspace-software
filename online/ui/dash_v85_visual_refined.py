import json
import numpy as np
import pandas as pd

from pathlib import Path
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

print("🚀 DASH V85 – SAFE MODE (SEM REGRESSÃO)")

BASE=Path(__file__).resolve().parents[3]

CSV_PATH=BASE/"products/final/grid_height.csv"
PLAN_PATH=BASE/"products/final/actuator_plan.json"

df=pd.read_csv(CSV_PATH)

rows=df["row"].max()+1
cols=df["col"].max()+1

grid=np.zeros((rows,cols))
for _,r in df.iterrows():
    grid[int(r["row"])][int(r["col"])]=r["z_cm"]

with open(PLAN_PATH) as f:
    plan=json.load(f)

events=plan["events"]

path=[]
heights=[]
current_pos=(0,0)

for e in events:
    if e["type"]=="move":
        current_pos=(e["row"],e["col"])
    if e["type"]=="set_height_cm":
        path.append(current_pos)
        heights.append(e["value_cm"])

app=Dash(__name__)

app.layout=html.Div([
    dcc.Graph(id="graph"),
    dcc.Interval(id="interval",interval=30,n_intervals=0)
])

@app.callback(
    Output("graph","figure"),
    Input("interval","n_intervals")
)
def update(n):

    step=n%len(path)

    z=grid.copy()

    if step<len(path):
        r,c=path[step]
        z[r][c]=heights[step]

    fig=go.Figure()

    # 🔹 HEATMAP ORIGINAL (NÃO ALTERAR)
    fig.add_trace(go.Heatmap(
        z=z,
        colorscale="Viridis",
        zmin=0,
        zmax=10,
        xgap=1,
        ygap=1,
        opacity=0.72,
        colorbar=dict(title="Altura (cm)")
    ))

    if step<len(path):
        # 🔹 HALO SUAVE (NÃO AFETA DADOS)
        fig.add_trace(go.Scatter(
            x=[c],y=[r],
            mode="markers",
            marker=dict(color="rgba(255,255,255,0.2)",size=36),
            showlegend=False
        ))

        # 🔹 PINO
        fig.add_trace(go.Scatter(
            x=[c],y=[r],
            mode="markers",
            marker=dict(color="white",size=10),
            showlegend=False
        ))

        # 🔹 BORDA DA CÉLULA (DESTAQUE SEM ALTERAR Z)
        fig.add_shape(
            type="rect",
            x0=c-0.5,x1=c+0.5,
            y0=r-0.5,y1=r+0.5,
            line=dict(color="white",width=2),
            layer="above"
        )

    fig.update_layout(
        width=900,
        height=450,
        margin=dict(l=0,r=0,t=0,b=0),
        plot_bgcolor="white",
        images=[dict(
            source="/assets/ipt_mask_rotated_simple.png",
            xref="x",yref="y",
            x=0,y=rows,
            sizex=cols,sizey=rows,
            sizing="stretch",
            opacity=0.18,
            layer="below"
        )]
    )

    return fig

if __name__=="__main__":
    app.run(debug=True)