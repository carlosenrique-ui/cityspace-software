import json
import base64
from io import BytesIO

import numpy as np
import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
from PIL import Image

PLAN_JSON = "/mnt/c/workspace/ipt-cityspace-engine/products/final/actuator_plan.json"
WATERMARK = "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/online/assets/ipt_mask_rotated_grid_aligned_v2.png"

# ============================================================
# AJUSTE SOMENTE DO WATERMARK
# Pinos/cores preservados
# Rotação em torno do centroide do conjunto colorido
# ============================================================
SCALE_X = 0.66
SCALE_Y = 0.58
OFFSET_X = -0.050
OFFSET_Y = 0.015
ROTATE_DEG = -8.8
WATERMARK_OPACITY = 0.28

nx, ny = 16, 8

# ============================================================
# LOAD PLAN
# ============================================================
with open(PLAN_JSON, "r", encoding="utf-8") as f:
    raw = json.load(f)

E = raw.get("events", raw) if isinstance(raw, dict) else raw

p = []
v = []
pos = (0, 0)

for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

p = [(min(r, 7), min(c, 15)) for r, c in p]

# ============================================================
# CENTROIDE DAS CORES
# ============================================================
colored = [(r, c) for (r, c), val in zip(p, v) if val > 0]

if colored:
    centroid_row = sum(r for r, c in colored) / len(colored)
    centroid_col = sum(c for r, c in colored) / len(colored)
else:
    centroid_row = 3.5
    centroid_col = 7.5

centroid_x_paper = (centroid_col + 0.5) / nx
centroid_y_paper = 1.0 - ((centroid_row + 0.5) / ny)

X = (1.0 - SCALE_X) / 2.0 + OFFSET_X
Y = 1.0 - (1.0 - SCALE_Y) / 2.0 + OFFSET_Y

# ============================================================
# WATERMARK: flip + padding + rotação sem corte
# ============================================================
img = Image.open(WATERMARK).convert("RGBA")
img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

w, h = img.size

pad_x = int(w * 1.0)
pad_y = int(h * 1.0)

canvas = Image.new(
    "RGBA",
    (w + 2 * pad_x, h + 2 * pad_y),
    (255, 255, 255, 0),
)
canvas.paste(img, (pad_x, pad_y), img)

# pivô equivalente ao centroide das cores dentro da imagem normalizada
pivot_x = pad_x + int(centroid_x_paper * w)
pivot_y = pad_y + int(centroid_y_paper * h)

rotated = canvas.rotate(
    ROTATE_DEG,
    resample=Image.Resampling.BICUBIC,
    expand=False,
    center=(pivot_x, pivot_y),
    fillcolor=(255, 255, 255, 0),
)

# crop alfa com margem grande para não cortar urbanismo
alpha = rotated.getchannel("A")
bbox = alpha.getbbox()
if bbox:
    margin = 140
    left = max(0, bbox[0] - margin)
    top = max(0, bbox[1] - margin)
    right = min(rotated.size[0], bbox[2] + margin)
    bottom = min(rotated.size[1], bbox[3] + margin)
    rotated = rotated.crop((left, top, right, bottom))

buf = BytesIO()
rotated.save(buf, format="PNG")
IMG = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ============================================================
# TIMELINE V96
# ============================================================
tl = [0.0]
for i in range(1, len(p)):
    dist = abs(p[i - 1][0] - p[i][0]) + abs(p[i - 1][1] - p[i][1])
    tl.append(tl[-1] + 0.2 * dist + 0.12 * abs(v[i]))

TMAX = tl[-1] if tl else 0.0

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph",
            config={"displayModeBar": False},
            style={"width": "100%", "height": "85vh"},
        ),
        html.Div(
            [
                html.Button("<<", id="back"),
                html.Button("Play", id="play"),
                html.Button("Pause", id="pause"),
                html.Button(">>", id="fwd"),
            ],
            style={"textAlign": "center"},
        ),
        dcc.Interval(id="interval", interval=60),
        dcc.Store(id="time", data=0.0),
        dcc.Store(id="running", data=False),
        dcc.Store(id="direction", data=1),
    ]
)


@app.callback(
    Output("running", "data"),
    Input("play", "n_clicks"),
    Input("pause", "n_clicks"),
    State("running", "data"),
    prevent_initial_call=True,
)
def cb_running(play_clicks, pause_clicks, running):
    if ctx.triggered_id == "play":
        return True
    if ctx.triggered_id == "pause":
        return False
    return running


@app.callback(
    Output("direction", "data"),
    Input("fwd", "n_clicks"),
    Input("back", "n_clicks"),
    State("direction", "data"),
    prevent_initial_call=True,
)
def cb_direction(fwd_clicks, back_clicks, direction):
    if ctx.triggered_id == "back":
        return -1
    if ctx.triggered_id == "fwd":
        return 1
    return direction


@app.callback(
    Output("time", "data"),
    Input("interval", "n_intervals"),
    State("running", "data"),
    State("direction", "data"),
    State("time", "data"),
)
def cb_time(n, running, direction, t):
    if not running:
        return t
    return max(0.0, min(TMAX, t + direction * 0.05))


def get_step(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


@app.callback(Output("graph", "figure"), Input("time", "data"))
def render_graph(t):
    s = get_step(t)

    Z = np.zeros((ny, nx), dtype=float)
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r, c] = v[i]

    fig = go.Figure()

    fig.update_layout(
        images=[
            dict(
                source=IMG,
                xref="paper",
                yref="paper",
                x=X,
                y=Y,
                sizex=SCALE_X,
                sizey=SCALE_Y,
                sizing="stretch",
                opacity=WATERMARK_OPACITY,
                layer="above",
            )
        ]
    )

    fig.add_trace(
        go.Heatmap(
            z=Z,
            colorscale="Jet",
            zmin=0,
            zmax=10,
            xgap=1,
            ygap=1,
            opacity=0.65,
            showscale=False,
        )
    )

    if s < len(p):
        r, c = p[s]
        fig.add_shape(
            type="rect",
            x0=c - 0.5,
            y0=r - 0.5,
            x1=c + 0.5,
            y1=r + 0.5,
            line=dict(color="white", width=2),
            fillcolor="rgba(255,255,255,0.25)",
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[-0.5, nx - 0.5], visible=False),
        yaxis=dict(range=[ny - 0.5, -0.5], visible=False, scaleanchor="x"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig


if __name__ == "__main__":
    print(">>> DASH V96 WATERMARK COLOR CENTROID <<<", flush=True)
    print(f"centroid_row={centroid_row}", flush=True)
    print(f"centroid_col={centroid_col}", flush=True)
    print(f"SCALE_X={SCALE_X}", flush=True)
    print(f"SCALE_Y={SCALE_Y}", flush=True)
    print(f"OFFSET_X={OFFSET_X}", flush=True)
    print(f"OFFSET_Y={OFFSET_Y}", flush=True)
    print(f"ROTATE_DEG={ROTATE_DEG}", flush=True)
    print(f"TMAX={TMAX}", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
