import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import os

FRAMES_DIR = "visualization/frames"
frames = sorted(os.listdir(FRAMES_DIR))
TOTAL = len(frames)

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("IPT CitySpace – V42 Player"),

    html.Img(id="frame", style={"width": "90%"}),

    dcc.Interval(id="interval", interval=200, n_intervals=0, disabled=True),

    html.Br(),

    html.Button("⏮ Back", id="back"),
    html.Button("▶ Play/Pause", id="play"),
    html.Button("⏭ Forward", id="forward"),

    dcc.Store(id="index", data=0),
    dcc.Store(id="playing", data=False)

])

# =========================================
# PLAY / PAUSE
# =========================================

@app.callback(
    Output("playing", "data"),
    Input("play", "n_clicks"),
    State("playing", "data")
)
def toggle_play(n, playing):
    if n:
        return not playing
    return playing

@app.callback(
    Output("interval", "disabled"),
    Input("playing", "data")
)
def control_interval(playing):
    return not playing

# =========================================
# AVANÇO AUTOMÁTICO
# =========================================

@app.callback(
    Output("index", "data"),
    Input("interval", "n_intervals"),
    State("index", "data")
)
def auto_play(n, idx):
    return (idx + 1) % TOTAL

# =========================================
# BOTÕES
# =========================================

@app.callback(
    Output("index", "data"),
    Input("forward", "n_clicks"),
    State("index", "data"),
    prevent_initial_call=True
)
def forward(n, idx):
    return (idx + 1) % TOTAL

@app.callback(
    Output("index", "data"),
    Input("back", "n_clicks"),
    State("index", "data"),
    prevent_initial_call=True
)
def back(n, idx):
    return (idx - 1) % TOTAL

# =========================================
# RENDER FRAME
# =========================================

@app.callback(
    Output("frame", "src"),
    Input("index", "data")
)
def update_frame(idx):
    return f"/assets/{frames[idx]}"

# =========================================

if __name__ == "__main__":
    app.run(debug=True)