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

nx, ny = 16, 8

DEFAULT_SCALE_X = 0.66
DEFAULT_SCALE_Y = 0.58
DEFAULT_OFFSET_X = -0.045
DEFAULT_OFFSET_Y = -0.030
DEFAULT_ROTATE = -8.8
DEFAULT_OPACITY = 0.28

with open(PLAN_JSON, "r", encoding="utf-8") as f:
    raw = json.load(f)

E = raw.get("events", raw)

p, v = [], []
pos = (0, 0)

for e in E:
    if e["type"] == "move":
        pos = (e["row"], e["col"])
    elif e["type"] == "set_height_cm":
        p.append(pos)
        v.append(e["value_cm"])

p = [(min(r, 7), min(c, 15)) for r, c in p]

tl = [0.0]
for i in range(1, len(p)):
    dist = abs(p[i - 1][0] - p[i][0]) + abs(p[i - 1][1] - p[i][1])
    tl.append(tl[-1] + 0.2 * dist + 0.12 * abs(v[i]))

TMAX = tl[-1] if tl else 0.0


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


def get_step(t):
    for i, x in enumerate(tl):
        if x >= t:
            return i
    return len(tl) - 1


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph",
            config={"displayModeBar": False},
            style={"width": "100%", "height": "76vh"},
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

        html.Div(
            [
                html.Div("SCALE_X"),
                dcc.Slider(id="scale_x", min=0.40, max=1.20, step=0.005, value=DEFAULT_SCALE_X),

                html.Div("SCALE_Y"),
                dcc.Slider(id="scale_y", min=0.40, max=1.20, step=0.005, value=DEFAULT_SCALE_Y),

                html.Div("OFFSET_X"),
                dcc.Slider(id="offset_x", min=-0.30, max=0.30, step=0.005, value=DEFAULT_OFFSET_X),

                html.Div("OFFSET_Y"),
                dcc.Slider(id="offset_y", min=-0.30, max=0.30, step=0.005, value=DEFAULT_OFFSET_Y),

                html.Div("ROTATE_DEG"),
                dcc.Slider(id="rotate_deg", min=-20.0, max=10.0, step=0.1, value=DEFAULT_ROTATE),

                html.Div("WATERMARK_OPACITY"),
                dcc.Slider(id="wm_opacity", min=0.05, max=0.70, step=0.01, value=DEFAULT_OPACITY),

                html.Pre(id="params_text", style={"fontSize": "16px", "fontWeight": "bold"}),
            ],
            style={"padding": "10px"},
        ),

        dcc.Interval(id="interval", interval=60),
        dcc.Store(id="time", data=TMAX),
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
def cb_running(a, b, running):
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
def cb_direction(a, b, direction):
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


@app.callback(
    Output("graph", "figure"),
    [
        Input("time", "data"),
        Input("scale_x", "value"),
        Input("scale_y", "value"),
        Input("offset_x", "value"),
        Input("offset_y", "value"),
        Input("rotate_deg", "value"),
        Input("wm_opacity", "value"),
    ],
)
def render_graph(*args):
    t, scale_x, scale_y, offset_x, offset_y, rotate_deg, wm_opacity = args

    s = get_step(t)

    Z = np.zeros((ny, nx), dtype=float)
    for i, (r, c) in enumerate(p):
        if i <= s:
            Z[r, c] = v[i]

    X = (1.0 - scale_x) / 2.0 + offset_x
    Y = 1.0 - ((1.0 - scale_y) / 2.0 + offset_y)

    fig = go.Figure()

    fig.update_layout(
        images=[
            dict(
                source=make_watermark(rotate_deg),
                xref="paper",
                yref="paper",
                x=X,
                y=Y,
                sizex=scale_x,
                sizey=scale_y,
                sizing="stretch",
                opacity=wm_opacity,
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


@app.callback(
    Output("params_text", "children"),
    [
        Input("scale_x", "value"),
        Input("scale_y", "value"),
        Input("offset_x", "value"),
        Input("offset_y", "value"),
        Input("rotate_deg", "value"),
        Input("wm_opacity", "value"),
    ],
)
def show_params(*args):
    scale_x, scale_y, offset_x, offset_y, rotate_deg, wm_opacity = args

    return (
        f"SCALE_X = {scale_x:.3f}\n"
        f"SCALE_Y = {scale_y:.3f}\n"
        f"OFFSET_X = {offset_x:.3f}\n"
        f"OFFSET_Y = {offset_y:.3f}\n"
        f"ROTATE_DEG = {rotate_deg:.1f}\n"
        f"WATERMARK_OPACITY = {wm_opacity:.2f}"
    )


if __name__ == "__main__":
    print(">>> DASH V96 WATERMARK CALIBRATOR FIXED <<<", flush=True)
    print(f"WATERMARK={WATERMARK}", flush=True)
    print(f"TMAX={TMAX}", flush=True)
    app.run(host="0.0.0.0", port=8050, debug=False)
