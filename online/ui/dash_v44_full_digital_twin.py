# ==========================================================
# IPT-CitySpace – V44 FULL DIGITAL TWIN (FÍSICO REAL)
# ==========================================================

import base64
import io
import math
import numpy as np
import matplotlib.pyplot as plt

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

# =========================================
# CONFIG (SUBSTITUIR PELOS SEUS CSV DEPOIS)
# =========================================

ROWS = 8
COLS = 16

ALTURA_MAX_PINO = 0.10

grid = np.random.rand(ROWS, COLS) * ALTURA_MAX_PINO
grid_z = np.random.rand(ROWS, COLS) * 40  # teto

estado = np.zeros_like(grid)

anos = np.linspace(1940, 2015, COLS).astype(int)

# =========================================
# FASES (IGUAL AO SEU)
# =========================================

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
    return "Fase", "#444", ""

# =========================================
# ZIGZAG REAL
# =========================================

def zigzag(rows, cols):
    traj = []
    for x in range(cols):
        ys = range(rows) if x % 2 == 0 else range(rows - 1, -1, -1)
        for y in ys:
            traj.append((x, y))
    return traj

traj = zigzag(ROWS, COLS)

# =========================================
# MOTION PROFILE (SIMPLIFICADO MAS REAL)
# =========================================

def motion_steps(h, steps=10):
    subida = np.linspace(0, h, steps)
    descida = np.linspace(h, 0, steps//2)
    return list(subida) + list(descida)

# =========================================
# RUNTIME STATE
# =========================================

class Runtime:

    def __init__(self):
        self.t = 0
        self.substep = 0
        self.local_steps = []
        self.estado = np.zeros_like(grid)

    def step(self):

        if self.t >= len(traj):
            return self.estado

        x, y = traj[self.t]
        altura = grid[y, x]

        # gerar steps locais
        if self.substep == 0:
            self.local_steps = motion_steps(altura)

        h = self.local_steps[self.substep]
        self.estado[y, x] = h

        self.substep += 1

        # terminou subida/descida → próximo ponto
        if self.substep >= len(self.local_steps):
            self.substep = 0
            self.t += 1

        return self.estado

runtime = Runtime()

# =========================================
# RENDER (IGUAL AO SEU)
# =========================================

def render_frame(estado, t):

    fig, ax = plt.subplots(figsize=(12,6))

    im = ax.imshow(
        estado,
        cmap="viridis",
        origin="upper",
        vmin=0,
        vmax=ALTURA_MAX_PINO,
        alpha=0.85
    )

    x_idx = min(t, COLS-1)
    ano = anos[x_idx]

    fase_nome, fase_cor, periodo = get_fase(ano)

    ax.set_title(
        f"IPT – CitySpace | {fase_nome} ({periodo})",
        fontsize=18,
        color=fase_cor
    )

    # eixo X progressivo
    ax.set_xticks(range(x_idx+1))
    ax.set_xticklabels(anos[:x_idx+1])

    ax.set_xlabel("Av. Escola Politécnica →", fontsize=14)
    ax.set_ylabel("USP →", fontsize=12)

    # COLORBAR PISO/TETO
    cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03)

    ticks = np.linspace(0, ALTURA_MAX_PINO, 6)
    labels = []

    for tck in ticks:
        teto = (tck / ALTURA_MAX_PINO) * grid_z.max()
        labels.append(f"{tck:.2f} / {teto:.2f}")

    cbar.set_ticks(ticks)
    cbar.set_ticklabels(labels)
    cbar.set_label("Pino / Teto (m)")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)

    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# =========================================
# DASH
# =========================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("IPT CitySpace – Digital Twin FULL"),

    html.Img(id="frame", style={"width":"100%"}),

    html.Div([
        html.Button("⏮ Backward", id="back"),
        html.Button("⏯ Play/Pause", id="play"),
        html.Button("⏭ Forward", id="forward"),
        html.Button("🔌 Mesa Física OFF", id="mesa")
    ]),

    dcc.Interval(id="clock", interval=120, disabled=True),

    dcc.Store(id="playing", data=False),
    dcc.Store(id="mesa_on", data=False)
])

# =========================================
# CONTROLE
# =========================================

@app.callback(
    Output("clock", "disabled"),
    Output("playing", "data"),
    Input("play", "n_clicks"),
    State("playing", "data"),
    prevent_initial_call=True
)
def toggle_play(n, playing):
    playing = not playing
    return not playing, playing

@app.callback(
    Output("mesa", "children"),
    Output("mesa_on", "data"),
    Input("mesa", "n_clicks"),
    State("mesa_on", "data"),
    prevent_initial_call=True
)
def toggle_mesa(n, estado):
    estado = not estado
    return ("🔌 Mesa Física ON" if estado else "🔌 Mesa Física OFF"), estado

# =========================================
# LOOP PRINCIPAL
# =========================================

@app.callback(
    Output("frame", "src"),
    Input("clock", "n_intervals")
)
def update(n):
    estado = runtime.step()
    return render_frame(estado, runtime.t)

# =========================================

if __name__ == "__main__":
    app.run(debug=True)