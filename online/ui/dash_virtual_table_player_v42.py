# ==========================================================
# IPT-CitySpace – Virtual Table Player (v42 FINAL LIMPO)
# ==========================================================

from pathlib import Path
import base64

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State


# =========================
# PATH + FRAMES
# =========================

ASSETS = Path(__file__).resolve().parents[2] / "assets"
FRAMES = sorted(ASSETS.glob("*.png"))

print("📂 ASSETS:", ASSETS)
print("📊 TOTAL FRAMES:", len(FRAMES))


def load_frame(idx):
    if not FRAMES:
        return ""

    frame = FRAMES[idx % len(FRAMES)]

    with open(frame, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    return f"data:image/png;base64,{encoded}"


# =========================
# DASH APP
# =========================

app = dash.Dash(__name__)


# =========================
# LAYOUT
# =========================

app.layout = html.Div([

    html.H2("IPT CitySpace – Virtual Table Player (REAL RENDER)"),

    html.Img(
        id="frame-player",
        src=load_frame(0),
        style={"width": "100%"}
    ),

    html.Div([
        html.Button("⏮ Backward", id="btn-back", n_clicks=0),
        html.Button("⏯ Play/Pause", id="btn-play", n_clicks=0),
        html.Button("⏭ Forward", id="btn-forward", n_clicks=0),
    ]),

    dcc.Interval(
        id="interval",
        interval=100,
        n_intervals=0,
        disabled=True
    ),

    dcc.Store(id="step", data=0),
    dcc.Store(id="playing", data=False)

])


# =========================
# CONTROLE CENTRAL (SEM DUPLICAÇÃO)
# =========================

@app.callback(
    Output("step", "data"),
    Output("interval", "disabled"),
    Output("playing", "data"),
    Input("btn-play", "n_clicks"),
    Input("btn-forward", "n_clicks"),
    Input("btn-back", "n_clicks"),
    Input("interval", "n_intervals"),
    State("step", "data"),
    State("playing", "data"),
    prevent_initial_call=True
)
def control(play, fwd, back, tick, step, playing):

    ctx = dash.callback_context

    if not ctx.triggered:
        return step, True, playing

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger == "btn-play":
        playing = not playing
        return step, not playing, playing

    if trigger == "btn-forward":
        return step + 1, True, False

    if trigger == "btn-back":
        return max(0, step - 1), True, False

    if trigger == "interval" and playing:
        return step + 1, False, playing

    return step, True, playing


# =========================
# RENDER FRAME
# =========================

@app.callback(
    Output("frame-player", "src"),
    Input("step", "data")
)
def render(step):
    return load_frame(step)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app.run(debug=True)