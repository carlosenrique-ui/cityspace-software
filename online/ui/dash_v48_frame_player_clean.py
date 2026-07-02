# ==========================================================
# IPT-CitySpace – V48 CLEAN (SEM QUEBRAR RENDER)
# ==========================================================

import base64
import io
from pathlib import Path
from PIL import Image

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# =========================================
# LOAD FRAMES (VERDADE VISUAL)
# =========================================

ASSETS = Path("assets")
frames = sorted(ASSETS.glob("frame_*.png"))

if not frames:
    raise RuntimeError("Nenhum frame encontrado em /assets")

images = [Image.open(f).convert("RGB") for f in frames]

print(f"[OK] Frames: {len(images)}")

# =========================================
# STATE
# =========================================

current = 0
running = False
direction = 1
mesa_on = False

# =========================================
# UTIL
# =========================================

def encode(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("IPT CitySpace – Virtual Table Player (REAL RENDER)"),

    html.Div(id="status"),

    html.Img(
        id="frame",
        src=encode(images[0]),
        style={
            "width": "100%",
            "maxWidth": "1400px",
        }
    ),

    html.Div([
        html.Button("⏮ Backward", id="back"),
        html.Button("⏯ Play/Pause", id="play"),
        html.Button("⏭ Forward", id="forward"),
        html.Button("🔌 Mesa Física OFF", id="mesa"),
    ]),

    dcc.Interval(id="clock", interval=80)
])

# =========================================
# CALLBACK ÚNICO (SEM DUPLICATE)
# =========================================

@app.callback(
    Output("frame", "src"),
    Output("status", "children"),
    Output("mesa", "children"),
    Input("clock", "n_intervals"),
    Input("play", "n_clicks"),
    Input("back", "n_clicks"),
    Input("forward", "n_clicks"),
    Input("mesa", "n_clicks"),
)
def update(_, play, back, forward, mesa):

    global current, running, direction, mesa_on

    ctx = dash.callback_context

    if ctx.triggered:
        btn = ctx.triggered[0]["prop_id"].split(".")[0]

        if btn == "play":
            running = not running

        elif btn == "back":
            direction = -1
            running = True

        elif btn == "forward":
            direction = 1
            running = True

        elif btn == "mesa":
            mesa_on = not mesa_on

    # avanço
    if running:
        current += direction

        if current < 0:
            current = 0
            running = False

        if current >= len(images):
            current = len(images)-1
            running = False

    status = (
        f"FRAME: {current}/{len(images)-1} | "
        f"RUN: {running} | DIR: {direction}"
    )

    mesa_label = "🔌 Mesa Física ON" if mesa_on else "🔌 Mesa Física OFF"

    return encode(images[current]), status, mesa_label

# =========================================

if __name__ == "__main__":
    app.run(debug=True)