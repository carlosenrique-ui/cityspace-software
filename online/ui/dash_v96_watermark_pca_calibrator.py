import json, base64, math
from io import BytesIO
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from PIL import Image

PLAN_JSON = "/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json"
WATERMARK = "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/online/assets/ipt_mask_rotated_grid_aligned_v2.png"

nx, ny = 16, 8

def pca_angle(points):
    pts = np.asarray(points, dtype=float)
    pts -= pts.mean(axis=0)
    cov = np.cov(pts.T)
    vals, vecs = np.linalg.eigh(cov)
    v = vecs[:, np.argmax(vals)]
    return math.degrees(math.atan2(v[1], v[0]))

with open(PLAN_JSON, "r", encoding="utf-8") as f:
    raw = json.load(f)

E = raw.get("events", raw)

p, v = [], []
pos = (0, 0)
for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append((min(pos[0], 7), min(pos[1], 15)))
        v.append(e["value_cm"])

Z = np.zeros((ny, nx))
for (r, c), val in zip(p, v):
    Z[r, c] = val

colored = [(c, r) for (r, c), val in zip(p, v) if val > 0]
angle_grid = pca_angle(colored) if len(colored) > 2 else 0.0

img0 = Image.open(WATERMARK).convert("RGBA")
img0 = img0.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
arr = np.array(img0)
dark = (arr[:, :, 3] > 20) & (arr[:, :, :3].mean(axis=2) < 245)
ys, xs = np.where(dark)
sample = np.column_stack([xs, ys])
if len(sample) > 5000:
    sample = sample[::len(sample)//5000]
angle_img = pca_angle(sample) if len(sample) > 2 else 0.0

AUTO_ROTATE = angle_grid - angle_img
AUTO_ROTATE = max(-20.0, min(10.0, AUTO_ROTATE))

DEFAULT_SCALE_X = 0.66
DEFAULT_SCALE_Y = 0.58
DEFAULT_OFFSET_X = -0.045
DEFAULT_OFFSET_Y = -0.030
DEFAULT_ROTATE = round(AUTO_ROTATE, 1)
DEFAULT_OPACITY = 0.28

def make_watermark(rotate_deg):
    img = Image.open(WATERMARK).convert("RGBA")
    img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img = img.rotate(
        rotate_deg,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(255, 255, 255, 0),
    )
    buf = BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def make_fig(scale_x, scale_y, offset_x, offset_y, rotate_deg, opacity):
    X = (1.0 - scale_x) / 2.0 + offset_x
    Y = 1.0 - ((1.0 - scale_y) / 2.0 + offset_y)

    fig = go.Figure()

    fig.update_layout(images=[dict(
        source=make_watermark(rotate_deg),
        xref="paper",
        yref="paper",
        x=X,
        y=Y,
        sizex=scale_x,
        sizey=scale_y,
        sizing="stretch",
        opacity=opacity,
        layer="above",
    )])

    fig.add_trace(go.Heatmap(
        z=Z,
        colorscale="Jet",
        zmin=0,
        zmax=10,
        xgap=1,
        ygap=1,
        opacity=0.65,
        showscale=False,
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[-0.5, nx - 0.5], visible=False),
        yaxis=dict(range=[ny - 0.5, -0.5], visible=False, scaleanchor="x"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="auto_graph", figure=make_fig(
        DEFAULT_SCALE_X, DEFAULT_SCALE_Y, DEFAULT_OFFSET_X,
        DEFAULT_OFFSET_Y, DEFAULT_ROTATE, DEFAULT_OPACITY
    ), config={"displayModeBar": False}, style={"height": "72vh"}),

    html.Pre(id="auto_params", children=(
        f"AUTO angle_grid={angle_grid:.2f}\n"
        f"AUTO angle_img={angle_img:.2f}\n"
        f"AUTO ROTATE_DEG={DEFAULT_ROTATE:.1f}\n"
    ), style={"fontSize": "15px", "fontWeight": "bold"}),

    html.Div("SCALE_X"),
    dcc.Slider(id="sx", min=0.40, max=1.20, step=0.005, value=DEFAULT_SCALE_X),

    html.Div("SCALE_Y"),
    dcc.Slider(id="sy", min=0.40, max=1.20, step=0.005, value=DEFAULT_SCALE_Y),

    html.Div("OFFSET_X"),
    dcc.Slider(id="ox", min=-0.30, max=0.30, step=0.005, value=DEFAULT_OFFSET_X),

    html.Div("OFFSET_Y"),
    dcc.Slider(id="oy", min=-0.30, max=0.30, step=0.005, value=DEFAULT_OFFSET_Y),

    html.Div("ROTATE_DEG"),
    dcc.Slider(id="rot", min=-20.0, max=10.0, step=0.1, value=DEFAULT_ROTATE),

    html.Div("WATERMARK_OPACITY"),
    dcc.Slider(id="op", min=0.05, max=0.70, step=0.01, value=DEFAULT_OPACITY),
])

@app.callback(
    Output("auto_graph", "figure"),
    Input("sx", "value"),
    Input("sy", "value"),
    Input("ox", "value"),
    Input("oy", "value"),
    Input("rot", "value"),
    Input("op", "value"),
)
def update(sx, sy, ox, oy, rot, op):
    print("PARAMS:",
          f"SCALE_X={sx:.3f}",
          f"SCALE_Y={sy:.3f}",
          f"OFFSET_X={ox:.3f}",
          f"OFFSET_Y={oy:.3f}",
          f"ROTATE_DEG={rot:.1f}",
          f"WATERMARK_OPACITY={op:.2f}",
          flush=True)
    return make_fig(sx, sy, ox, oy, rot, op)

if __name__ == "__main__":
    print(">>> DASH V96 PCA WATERMARK CALIBRATOR <<<", flush=True)
    print(f"WATERMARK={WATERMARK}", flush=True)
    print(f"angle_grid={angle_grid:.2f}", flush=True)
    print(f"angle_img={angle_img:.2f}", flush=True)
    print(f"AUTO_ROTATE={DEFAULT_ROTATE:.1f}", flush=True)
    app.run(host="0.0.0.0", port=8052, debug=False)
