# ==========================================================
# IPT-CitySpace – V47 (FINAL VISUAL + ESCALA FÍSICA)
# ==========================================================

import base64
import io
from pathlib import Path
from PIL import Image

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# =========================================
# CONFIG FÍSICA
# =========================================

SCALE = 1.0   # 1.0 | 2.0 | 0.5

# =========================================
# ANOS + FASES
# =========================================

COLS = 16

anos = list(range(1940, 1940 + COLS))

FASES = [
    (1940, 1959, "Implantação na USP", "#2E86C1"),
    (1960, 1979, "Expansão", "#239B56"),
    (1980, 1999, "Consolidação", "#C0392B"),
    (2000, 2015, "Inovação", "#E67E22"),
]

def get_fase(ano):
    for i, f, nome, cor in FASES:
        if i <= ano <= f:
            return nome, cor, f"{i}-{f}"
    return "", "#000", ""

# =========================================
# LOAD FRAMES
# =========================================

ASSETS = Path("assets")
frames = sorted(ASSETS.glob("frame_*.png"))

if not frames:
    raise RuntimeError("Nenhum frame encontrado")

images = [Image.open(f).convert("RGB") for f in frames]

print("Frames:", len(images))

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

    # escala física
    w, h = img.size
    img = img.resize((int(w*SCALE), int(h*SCALE)))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div(

    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
    },

    children=[

        html.H2(id="title"),

        html.Div(id="status"),

        html.Img(
            id="frame",
            src=encode(images[0]),
            style={
                "width": "90%",
                "maxWidth": "1400px",
                "border": "1px solid black"
            }
        ),

        html.Div(
            "USP ↑",
            style={"fontWeight": "bold", "marginTop": "5px"}
        ),

        html.Div(
            "Av. Escola Politécnica →",
            style={"fontWeight": "bold"}
        ),

        html.Div([
            html.Button("⏮ Backward", id="back"),
            html.Button("⏯ Play/Pause", id="play"),
            html.Button("⏭ Forward", id="forward"),
            html.Button("🔌 Mesa Física OFF", id="mesa"),
        ]),

        dcc.Interval(id="clock", interval=80)
    ]
)

# =========================================
# CALLBACK
# =========================================

@app.callback(
    Output("frame", "src"),
    Output("status", "children"),
    Output("mesa", "children"),
    Output("title", "children"),
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

    # ANO DINÂMICO
    col = min(current, COLS-1)
    ano = anos[col]

    fase, cor, periodo = get_fase(ano)

    title = f"IPT – CitySpace | {fase} ({periodo})"

    status = f"FRAME: {current}/{len(images)-1} | ANO: {ano}"

    mesa_label = "🔌 Mesa Física ON" if mesa_on else "🔌 Mesa Física OFF"

    return encode(images[current]), status, mesa_label, title

# =========================================

if __name__ == "__main__":
    app.run(debug=True)