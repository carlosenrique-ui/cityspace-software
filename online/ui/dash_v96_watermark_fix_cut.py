import json, base64
from io import BytesIO
import numpy as np, pandas as pd, dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
from PIL import Image

GRID_CSV = "/mnt/c/workspace/ipt-cityspace-engine/products/final/grid_height.csv"
PLAN_JSON = "/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json"
WATERMARK = "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/online/assets/ipt_mask_rotated_grid_aligned_v2.png"

# ============================================================
# AJUSTE FINAL
# ============================================================
SCALE_X = 0.66
SCALE_Y = 0.58
OFFSET_X = -0.045
OFFSET_Y = -0.030
ROTATE_DEG = -8.8
WATERMARK_OPACITY = 0.28

X = (1 - SCALE_X)/2 + OFFSET_X
Y = 1 - (1 - SCALE_Y)/2 + OFFSET_Y

# ============================================================
# LOAD + ROTATE (SEM CORTE)
# ============================================================
img = Image.open(WATERMARK).convert("RGBA")
img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

img = img.rotate(
    ROTATE_DEG,
    resample=Image.Resampling.BICUBIC,
    expand=True,  # <<< CORRIGE CORTE
    fillcolor=(255,255,255,0)
)

buf = BytesIO()
img.save(buf, format="PNG")
IMG = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ============================================================
# DATA
# ============================================================
with open(PLAN_JSON) as f:
    E = json.load(f).get("events")

p,v,pos=[],[],(0,0)
for e in E:
    if e["type"]=="move": pos=(e["row"],e["col"])
    elif e["type"]=="set_height_cm":
        p.append(pos); v.append(e["value_cm"])

p=[(min(r,7),min(c,15)) for r,c in p]

tl=[0]
for i in range(1,len(p)):
    tl.append(tl[-1]+0.2*(abs(p[i-1][0]-p[i][0])+abs(p[i-1][1]-p[i][1]))+0.12*abs(v[i]))

TMAX=tl[-1] if tl else 0
nx,ny=16,8

app=dash.Dash(__name__)

app.layout=html.Div([
    dcc.Graph(id="g",config={"displayModeBar":False},style={"height":"85vh"}),
    html.Div([
        html.Button("<<",id="b"),
        html.Button("Play",id="p"),
        html.Button("Pause",id="pa"),
        html.Button(">>",id="f"),
    ],style={"textAlign":"center"}),
    dcc.Interval(id="i",interval=60),
    dcc.Store(id="t",data=0),
    dcc.Store(id="r",data=False),
    dcc.Store(id="d",data=1)
])

@app.callback(Output("r","data"),Input("p","n_clicks"),Input("pa","n_clicks"),State("r","data"),prevent_initial_call=True)
def _(a,b,c): return True if ctx.triggered_id=="p" else False if ctx.triggered_id=="pa" else c

@app.callback(Output("d","data"),Input("f","n_clicks"),Input("b","n_clicks"),State("d","data"),prevent_initial_call=True)
def _(a,b,c): return -1 if ctx.triggered_id=="b" else 1 if ctx.triggered_id=="f" else c

@app.callback(Output("t","data"),Input("i","n_intervals"),State("r","data"),State("d","data"),State("t","data"))
def _(n,r,d,t): return t if not r else max(0,min(TMAX,t+d*0.05))

def gs(t):
    for i,x in enumerate(tl):
        if x>=t: return i
    return len(tl)-1

@app.callback(Output("g","figure"),Input("t","data"))
def _(t):
    s=gs(t)
    Z=np.zeros((ny,nx))
    for i,(r,c) in enumerate(p):
        if i<=s: Z[r][c]=v[i]

    fig=go.Figure()

    fig.update_layout(images=[dict(
        source=IMG,xref="paper",yref="paper",
        x=X,y=Y,sizex=SCALE_X,sizey=SCALE_Y,
        sizing="stretch",opacity=WATERMARK_OPACITY,layer="above"
    )])

    fig.add_trace(go.Heatmap(
        z=Z,colorscale="Jet",zmin=0,zmax=10,
        xgap=1,ygap=1,opacity=0.65,showscale=False
    ))

    fig.update_layout(
        margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(range=[-0.5,nx-0.5],visible=False),
        yaxis=dict(range=[ny-0.5,-0.5],visible=False,scaleanchor="x"),
    )

    return fig

if __name__=="__main__":
    print(">>> FIX CUT + ROTATION <<<")
    app.run(host="0.0.0.0",port=8050,debug=False)
