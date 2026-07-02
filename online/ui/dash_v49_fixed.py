# ==========================================================
# IPT-CitySpace – V49 FIX (ANIMAÇÃO REAL + SEM DUPLICATE)
# ==========================================================

import base64
import io
import threading
import time
from pathlib import Path
from PIL import Image

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# =========================================
# LOAD FRAMES
# =========================================

ASSETS = Path("assets")
frames = sorted(ASSETS.glob("frame_*.png"))

if not frames:
    raise RuntimeError("Nenhum frame encontrado")

images = [Image.open(f).convert("RGB") for f in frames]
TOTAL = len(images)

print(f"[OK] Frames: {TOTAL}")

# =========================================
# CLOCK GLOBAL
# =========================================

class Clock:
    def __init__(self):
        self.index = 0
        self.running = False
        self.direction = 1
        self.lock = threading.Lock()

    def update(self):
        with self.lock:
            if self.running:
                self.index += self.direction

                if self.index < 0:
                    self.index = 0
                    self.running = False

                if self.index >= TOTAL:
                    self.index = TOTAL - 1
                    self.running = False

clock = Clock()

# =========================================
# THREAD DE TEMPO
# =========================================

def loop():
    while True:
        clock.update()
        time.sleep(0.08)

threading.Thread(target=loop, daemon=True).start()

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

    html.H2("IPT CitySpace – Virtual Table (CORE SYNC FIX)"),

    html.Div(id="status"),

    html.Img(
        id="frame",
        src=encode(images[0]),
        style={"width": "100%", "maxWidth": "1400px"}
    ),

    html.Div([
        html.Button("⏮ Backward", id="back"),
        html.Button("⏯ Play/Pause", id="play"),
        html.Button("⏭ Forward", id="forward"),
    ]),

    dcc.Interval(id="tick", interval=80)
])

# =========================================
# CALLBACK ÚNICO (CORRETO)
# =========================================

@app.callback(
    Output("frame", "src"),
    Output("status", "children"),
    Input("tick", "n_intervals"),
    Input("play", "n_clicks"),
    Input("back", "n_clicks"),
    Input("forward", "n_clicks"),
)
def update(_, play, back, forward):

    ctx = dash.callback_context

    if ctx.triggered:
        btn = ctx.triggered[0]["prop_id"].split(".")[0]

        if btn == "play":
            clock.running = not clock.running

        elif btn == "back":
            clock.direction = -1
            clock.running = True

        elif btn == "forward":
            clock.direction = 1
            clock.running = True

    idx = clock.index

    status = (
        f"FRAME: {idx}/{TOTAL-1} | "
        f"RUN: {clock.running} | DIR: {clock.direction}"
    )

    return encode(images[idx]), status

# =========================================

if __name__ == "__main__":
    app.run(debug=True)