# ==========================================================
# IPT-CitySpace – V49 (FRAME + CORE SINCRONIZADO)
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
# CLOCK REAL (SUBSTITUI CONTADOR BURRO)
# =========================================

class Clock:
    def __init__(self):
        self.index = 0
        self.running = False
        self.direction = 1
        self.lock = threading.Lock()

    def play(self):
        self.running = True

    def pause(self):
        self.running = False

    def forward(self):
        self.direction = 1
        self.running = True

    def backward(self):
        self.direction = -1
        self.running = True

    def step(self):
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
# THREAD DE TEMPO (SIMULA TEMPORAL CORE)
# =========================================

def loop():
    while True:
        clock.step()
        time.sleep(0.08)  # 🔥 tempo REAL do sistema

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

    html.H2("IPT CitySpace – Virtual Table (CORE SYNC)"),

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

    dcc.Interval(id="refresh", interval=80)
])

# =========================================
# CONTROLES
# =========================================

@app.callback(
    Output("status", "children"),
    Input("play", "n_clicks"),
    Input("back", "n_clicks"),
    Input("forward", "n_clicks"),
    prevent_initial_call=True
)
def control(play, back, forward):

    ctx = dash.callback_context
    btn = ctx.triggered[0]["prop_id"].split(".")[0]

    if btn == "play":
        if clock.running:
            clock.pause()
        else:
            clock.play()

    elif btn == "back":
        clock.backward()

    elif btn == "forward":
        clock.forward()

    return dash.no_update

# =========================================
# VIEW (OBSERVADOR)
# =========================================

@app.callback(
    Output("frame", "src"),
    Output("status", "children"),
    Input("refresh", "n_intervals"),
)
def update(_):

    idx = clock.index

    status = (
        f"FRAME: {idx}/{TOTAL-1} | "
        f"RUN: {clock.running} | DIR: {clock.direction}"
    )

    return encode(images[idx]), status

# =========================================

if __name__ == "__main__":
    app.run(debug=True)