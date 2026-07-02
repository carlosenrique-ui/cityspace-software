# ==========================================================
# IPT-CitySpace – UI V47 (CORRETO E INCREMENTAL)
# ==========================================================

import base64
import io
from pathlib import Path
from PIL import Image, ImageDraw

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

BASE = Path("/mnt/c/workspace/ipt-cityspace-engine")
ASSETS = BASE / "assets"

frames = sorted(ASSETS.glob("frame_*.png"))
images = [Image.open(f).convert("RGB") for f in frames]

ROWS = 8
COLS = 16

# zigzag (igual render)
def zigzag():
    traj = []
    for x in range(COLS):
        ys = range(ROWS) if x % 2 == 0 else range(ROWS-1, -1, -1)
        for y in ys:
            traj.append((x, y))
    return traj

traj = zigzag()

FRAMES_PER_PIN = len(images) // len(traj)

# =========================================
# STATE
# =========================================

current = 0
running = False
direction = 1
mesa_on = False

# =========================================
# OVERLAY (SÓ HIGHLIGHT)
# =========================================

def overlay(img, frame):

    img = img.copy()
    draw = ImageDraw.Draw(img)

    w, h = img.size
    cell_w = w / COLS
    cell_h = h / ROWS

    idx = frame // FRAMES_PER_PIN
    idx = min(idx, len(traj)-1)

    x, y = traj[idx]

    x0 = int(x * cell_w)
    y0 = int(y * cell_h)
    x1 = int((x+1) * cell_w)
    y1 = int((y+1) * cell_h)

    draw.rectangle([x0, y0, x1, y1], outline="white", width=3)

    return img

# =========================================
# ENCODE
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

    html.H2("IPT CitySpace – Virtual Table Player (FINAL)"),

    html.Img(id="frame", style={"width":"100%"}),

    html.Div([
        html.Button("⏮ Backward", id="back"),
        html.Button("⏯ Play/Pause", id="play"),
        html.Button("⏭ Forward", id="forward"),
        html.Button("🔌 Mesa Física OFF", id="mesa"),
    ]),

    dcc.Interval(id="clock", interval=80)
])

# =========================================
# CALLBACK
# =========================================

@app.callback(
    Output("frame", "src"),
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

    if running:
        current += direction

        if current < 0:
            current = 0
            running = False

        if current >= len(images):
            current = len(images)-1
            running = False

    frame = overlay(images[current], current)

    mesa_label = "🔌 Mesa Física ON" if mesa_on else "🔌 Mesa Física OFF"

    return encode(frame), mesa_label

# =========================================

if __name__ == "__main__":
    app.run(debug=True)