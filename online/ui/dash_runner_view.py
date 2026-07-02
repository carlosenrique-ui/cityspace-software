import threading
import time

import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from online.runtime.plan_execution_runner import PlanExecutionRunner

# =========================================
# LOAD PLAN
# =========================================
runner = PlanExecutionRunner("products/latest/actuator_plan.json")

grid = np.zeros((10, 10))  # ajuste depois se quiser dinâmico

running = False

# =========================================
# LOOP
# =========================================
def loop():
    global running

    while True:
        if running:
            event = runner.step()

            if event:
                if event["type"] == "move":
                    loop.x = event["col"]
                    loop.y = event["row"]

                elif event["type"] == "set_height_cm":
                    grid[loop.y, loop.x] = event["value_cm"] / 100.0

        time.sleep(0.05)

loop.x = 0
loop.y = 0

threading.Thread(target=loop, daemon=True).start()

# =========================================
# DASH
# =========================================
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button("Play", id="play"),
    dcc.Graph(id="grid"),
    dcc.Interval(id="tick", interval=200)
])

@app.callback(
    Output("play", "n_clicks"),
    Input("play", "n_clicks"),
    prevent_initial_call=True
)
def toggle(n):
    global running
    running = not running
    return n

@app.callback(
    Output("grid", "figure"),
    Input("tick", "n_intervals")
)
def update(_):
    fig = px.imshow(grid, color_continuous_scale="Viridis")
    fig.update_layout(yaxis_autorange="reversed")
    return fig

if __name__ == "__main__":
    app.run(debug=False)
