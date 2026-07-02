import base64
import io

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from PIL import Image

from online.renderers.renderer_factory import get_gif_path

# =====================================================
# CONFIG
# =====================================================

VERSION = "v41"
GIF_PATH = get_gif_path(VERSION)

# =====================================================
# LOAD GIF
# =====================================================

frames = []

gif = Image.open(GIF_PATH)

for i in range(getattr(gif, "n_frames", 1)):
    gif.seek(i)
    frames.append(gif.convert("RGB").copy())

print("[DEBUG] Frames carregados:", len(frames))

if len(frames) == 0:
    raise RuntimeError("Nenhum frame carregado.")

# =====================================================
# STATE SIMPLES (sem core ainda)
# =====================================================

current_index = 0
running = False
direction = 1

# =====================================================
# UTIL
# =====================================================

def encode_pil(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return "data:image/png;base64," + \
        base64.b64encode(buffer.getvalue()).decode()

# =====================================================
# DASH APP
# =====================================================

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "width": "100%",
    },
    children=[

        html.H2("IPT – CitySpace | Mesa Virtual (v41)"),

        html.Div(id="status"),

        html.Img(
            id="frame-view",
            src=encode_pil(frames[0]),
            style={
                "width": "100%",
                "maxWidth": "1000px",
                "border": "1px solid black",
                "marginBottom": "10px",
            },
        ),

        html.Div(
            style={
                "display": "flex",
                "gap": "8px",
                "justifyContent": "center",
            },
            children=[
                html.Button("▶ Play", id="btn-play"),
                html.Button("⏸ Pause", id="btn-pause"),
                html.Button("⏮ Backward", id="btn-backward"),
                html.Button("↺ Reset", id="btn-reset"),
            ],
        ),

        dcc.Interval(id="tick", interval=150)
    ],
)

# =====================================================
# CALLBACK ÚNICO
# =====================================================

@app.callback(
    Output("status", "children"),
    Output("frame-view", "src"),
    Input("btn-play", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-backward", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    Input("tick", "n_intervals"),
)
def update(play, pause, backward, reset, _):

    global current_index, running, direction

    ctx = dash.callback_context

    if ctx.triggered:
        source = ctx.triggered[0]["prop_id"].split(".")[0]

        if source == "btn-play":
            running = True
            direction = 1

        elif source == "btn-pause":
            running = False

        elif source == "btn-backward":
            running = True
            direction = -1

        elif source == "btn-reset":
            running = False
            current_index = 0

    # avanço simples
    if running:
        current_index += direction

        if current_index < 0:
            current_index = 0
            running = False

        if current_index >= len(frames):
            current_index = len(frames) - 1
            running = False

    status = (
        f"INDEX: {current_index} / {len(frames)-1} | "
        f"DIRECTION: {direction} | "
        f"RUNNING: {running}"
    )

    return status, encode_pil(frames[current_index])

# =====================================================
if __name__ == "__main__":
    app.run(debug=False)
