from dash import Dash, html, dcc, Input, Output, State, ctx
import dash

# -------------------------------------------------
# Configurações básicas
# -------------------------------------------------
MAX_FRAMES = 128

app = Dash(__name__)

# -------------------------------------------------
# Layout
# -------------------------------------------------
app.layout = html.Div(
    style={"padding": "20px"},
    children=[
        html.H2("IPT CitySpace — Player 2D (Virtual)"),

        # -----------------------------
        # Controles
        # -----------------------------
        html.Div(
            [
                html.Button("▶ Play", id="btn-play"),
                html.Button("⏸ Pause", id="btn-pause"),
                html.Button("⏹ Stop", id="btn-stop"),
                html.Button("⏮ Step -", id="btn-step-prev"),
                html.Button("⏭ Step +", id="btn-step-next"),
            ],
            style={"marginBottom": "10px"},
        ),

        # -----------------------------
        # Timeline
        # -----------------------------
        dcc.Slider(
            id="timeline",
            min=0,
            max=MAX_FRAMES - 1,
            step=1,
            value=0,
            marks={i: str(i) for i in range(0, MAX_FRAMES, 8)},
        ),

        # -----------------------------
        # Interval (player automático)
        # -----------------------------
        dcc.Interval(
            id="player-interval",
            interval=500,  # ms
            disabled=True,
        ),

        # -----------------------------
        # Estado central do player
        # -----------------------------
        dcc.Store(
            id="player-state",
            data={"mode": "STOP", "frame": 0},
        ),

        html.Hr(),

        html.Pre(id="debug", style={"fontSize": "12px"}),
    ],
)

# -------------------------------------------------
# Callback ÚNICO de controle do player
# -------------------------------------------------
@app.callback(
    Output("player-state", "data"),
    Output("timeline", "value"),
    Output("player-interval", "disabled"),
    Output("debug", "children"),
    Input("btn-play", "n_clicks"),
    Input("btn-pause", "n_clicks"),
    Input("btn-stop", "n_clicks"),
    Input("btn-step-prev", "n_clicks"),
    Input("btn-step-next", "n_clicks"),
    Input("player-interval", "n_intervals"),
    State("player-state", "data"),
    prevent_initial_call=True,
)
def control_player(
    n_play,
    n_pause,
    n_stop,
    n_prev,
    n_next,
    n_intervals,
    state,
):
    trigger = ctx.triggered_id

    mode = state["mode"]
    frame = state["frame"]

    # -----------------------------
    # Eventos de botão
    # -----------------------------
    if trigger == "btn-play":
        mode = "PLAY"

    elif trigger == "btn-pause":
        mode = "PAUSE"

    elif trigger == "btn-stop":
        mode = "STOP"
        frame = 0

    elif trigger == "btn-step-prev":
        frame = max(0, frame - 1)
        mode = "PAUSE"

    elif trigger == "btn-step-next":
        frame = min(MAX_FRAMES - 1, frame + 1)
        mode = "PAUSE"

    # -----------------------------
    # Evento de tempo (PLAY)
    # -----------------------------
    elif trigger == "player-interval" and mode == "PLAY":
        frame += 1
        if frame >= MAX_FRAMES:
            frame = MAX_FRAMES - 1
            mode = "PAUSE"

    # -----------------------------
    # Controle do interval
    # -----------------------------
    interval_disabled = mode != "PLAY"

    new_state = {
        "mode": mode,
        "frame": frame,
    }

    debug_text = (
        f"Trigger: {trigger}\n"
        f"Mode: {mode}\n"
        f"Frame: {frame}"
    )

    return new_state, frame, interval_disabled, debug_text


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
