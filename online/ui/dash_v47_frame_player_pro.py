# ==========================================================
# IPT-CitySpace – V47 FRAME PLAYER PRO
# (UI corrigida + escala física + timeline real)
# ==========================================================

import base64
import io
from pathlib import Path
from PIL import Image

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# =========================================
# CONFIG TEMPORAL (AJUSTE FINO)
# =========================================

START_YEAR = 1940
END_YEAR   = 2020

PHASES = [
    (1940, 1959, "Formação"),
    (1960, 1979, "Expansão"),
    (1980, 1999, "Consolidação"),
    (2000, 2020, "Modernização"),
]

# =========================================
# LOAD FRAMES
# =========================================

ASSETS = Path("assets")
frames = sorted(ASSETS.glob("frame_*.png"))

if not frames:
    raise RuntimeError("Nenhum frame encontrado em /assets")

images = [Image.open(f).convert("RGB") for f in frames]

print(f"📊 Frames carregados: {len(images)}")

# =========================================
# STATE GLOBAL
# =========================================

current = 0
running = False
direction = 1
mesa_on = False
scale = 1.0  # 🔥 NOVO (escala física)

# =========================================
# UTIL
# =========================================

def encode(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def get_year(index):
    total = len(images)
    return int(START_YEAR + (index / (total - 1)) * (END_YEAR - START_YEAR))

def get_phase(year):
    for start, end, name in PHASES:
        if start <= year <= end:
            return f"{name} ({start}-{end})"
    return "N/A"

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div(

    style={
        "backgroundColor": "#111",
        "color": "white",
        "textAlign": "center",
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center"
    },

    children=[

        html.H2(id="title"),

        html.Div(id="status"),

        html.Div(
            style={
                "position": "relative",
                "display": "inline-block"
            },
            children=[

                # 🔥 FRAME CENTRALIZADO + ESCALA
                html.Img(
                    id="frame",
                    src=encode(images[0]),
                    style={
                        "width": f"{int(100 * scale)}%",
                        "maxWidth": "1200px",
                        "border": "2px solid #444"
                    }
                ),

                # 🔥 ORIENTAÇÃO (CRÍTICO)
                html.Div("USP ↑", style={
                    "position": "absolute",
                    "top": "10px",
                    "left": "50%",
                    "transform": "translateX(-50%)",
                    "fontSize": "14px",
                    "opacity": 0.7
                }),

                html.Div("Av. Escola Politécnica →", style={
                    "position": "absolute",
                    "right": "10px",
                    "top": "50%",
                    "transform": "translateY(-50%) rotate(90deg)",
                    "fontSize": "14px",
                    "opacity": 0.7
                }),

            ]
        ),

        # 🔥 TIMELINE (ANOS)
        html.Div(id="timeline", style={
            "marginTop": "10px",
            "fontSize": "14px",
            "opacity": 0.8
        }),

        html.Br(),

        html.Div([
            html.Button("⏮", id="back"),
            html.Button("⏯", id="play"),
            html.Button("⏭", id="forward"),
            html.Button("🔌 Mesa OFF", id="mesa"),
            html.Button("🔍 Escala 1x", id="scale"),
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
    Output("title", "children"),
    Output("timeline", "children"),
    Output("mesa", "children"),
    Output("scale", "children"),
    Input("clock", "n_intervals"),
    Input("play", "n_clicks"),
    Input("back", "n_clicks"),
    Input("forward", "n_clicks"),
    Input("mesa", "n_clicks"),
    Input("scale", "n_clicks"),
)
def update(_, play, back, forward, mesa, scale_btn):

    global current, running, direction, mesa_on, scale

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

        elif btn == "scale":
            # 🔥 CICLO DE ESCALA FÍSICA
            if scale == 1.0:
                scale = 2.0
            elif scale == 2.0:
                scale = 0.5
            else:
                scale = 1.0

    # avanço
    if running:
        current += direction

        if current < 0:
            current = 0
            running = False

        if current >= len(images):
            current = len(images) - 1
            running = False

    # 🔥 METADATA
    year = get_year(current)
    phase = get_phase(year)

    title = f"IPT – CitySpace | {phase} | {year}"

    timeline = f"{START_YEAR} ───── {year} ───── {END_YEAR}"

    status = f"FRAME: {current}/{len(images)-1}"

    mesa_label = "🔌 Mesa ON" if mesa_on else "🔌 Mesa OFF"
    scale_label = f"🔍 Escala {scale}x"

    return (
        encode(images[current]),
        status,
        title,
        timeline,
        mesa_label,
        scale_label
    )

# =========================================

if __name__ == "__main__":
    app.run(debug=True)