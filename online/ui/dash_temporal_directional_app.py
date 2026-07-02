import base64
from pathlib import Path

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from online.core.temporal_core_directional import TemporalCoreDirectional

# =====================================================
# FRAMES (V41 / DEBUG)
# =====================================================

FRAMES_DIR = Path("visualization/debug")
frames = sorted(FRAMES_DIR.glob("*.png"))

if not frames:
    raise RuntimeError("Nenhum frame PNG encontrado em visualization/debug")

# =====================================================
# CORE
# =====================================================

core = TemporalCoreDirectional(max_index=len(frames) - 1)

# =====================================================
# UTIL
# =====================================================

def encode_image(path: Path):
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"

# =====================================================
# DASH APP
# =====================================================

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("IPT-CitySpace — Temporal Controls"),

    html.Div(id="status", style={"marginBottom": "10px"}),

    html.Img(
        id="frame-view",
        style={
            "width": "900px",
            "border": "1px solid black",
            "marginBottom": "10px"
        }
    ),

    html.Button("▶ Play", id="btn-play"),
    html.Button("⏮ Backward", id="btn-backward"),
    html.Button("⏸ Pause", id="btn-pause"),
    html.Button("↺ Reset", id="btn-reset"),

    dcc.Interval(id="tick", interval=100)
])

# =====================================================
# CALLBACK
# =====================================================

@app.callback(
    Output("status", "children"),
    Output("frame-view", "src"),
    Input("btn-play", "n_clicks"),
    Input("btn-backward", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-reset", "n_clicks"),
    Input("tick", "n_intervals"),
)
def control(play, backward, pause, reset, _):

    ctx = dash.callback_context

    if ctx.triggered:
        source = ctx.triggered[0]["prop_id"].split(".")[0]

        if source == "btn-play":
            core.play_forward()

        elif source == "btn-backward":
            core.play_backward()

        elif source == "btn-pause":
            core.pause()

        elif source == "btn-reset":
            core.reset()

    core.tick()

    status = (
        f"INDEX: {core.index} / {core.max_index} | "
        f"DIRECTION: {core.direction} | "
        f"RUNNING: {core.running}"
    )

    img = encode_image(frames[core.index])

    return status, img

# =====================================================
if __name__ == "__main__":
    app.run(debug=False)
