from pathlib import Path
import json

from dash import Dash, html, dcc, Input, Output


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"

SPATIAL_LAYOUT_FILE = CONTRACTS / "spatial_layout_16x8.json"
PHYSICAL_CONTRACT_FILE = CONTRACTS / "physical_table_contract.json"


with open(SPATIAL_LAYOUT_FILE, "r", encoding="utf-8") as f:
    spatial_layout = json.load(f)

with open(PHYSICAL_CONTRACT_FILE, "r", encoding="utf-8") as f:
    physical_contract = json.load(f)


ROWS = spatial_layout["rows"]
COLS = spatial_layout["cols"]
PINS = spatial_layout["pins"]

PIN_BY_RC = {
    (p["row"], p["col"]): p
    for p in PINS
}


app = Dash(__name__)

app.title = "Globe-CitySpace Physical Table"


app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Globe-CitySpace — Physical Table Preview"),
                html.Div("G5.2 • Spatial Layout oficial IPT-CitySpace"),
            ],
        ),

        html.Div(
            className="controls",
            children=[
                html.Label("Tamanho da célula física"),
                dcc.RadioItems(
                    id="cell-size",
                    options=[
                        {"label": "1 cm x 1 cm", "value": 1},
                        {"label": "2 cm x 2 cm", "value": 2},
                    ],
                    value=physical_contract.get("default_cell_size_cm", 2),
                    inline=True,
                ),
            ],
        ),

        html.Div(
            className="content",
            children=[
                html.Div(
                    id="table-info",
                    className="info",
                ),
                html.Div(
                    id="physical-table",
                    className="physical-table",
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("physical-table", "children"),
    Output("table-info", "children"),
    Input("cell-size", "value"),
)
def render_table(cell_size_cm):
    table_width_cm = COLS * cell_size_cm
    table_height_cm = ROWS * cell_size_cm

    cells = []

    for row in range(1, ROWS + 1):
        for col in range(1, COLS + 1):
            pin = PIN_BY_RC[(row, col)]

            classes = ["cell"]

            if pin["cell_id"] == "P001":
                classes.append("corner-start")
            if pin["cell_id"] == "P016":
                classes.append("corner-top-right")
            if pin["cell_id"] == "P113":
                classes.append("corner-bottom-left")
            if pin["cell_id"] == "P128":
                classes.append("corner-end")

            cells.append(
                html.Div(
                    className=" ".join(classes),
                    children=[
                        html.Strong(pin["cell_id"]),
                        html.Span(f"L{row} C{col}"),
                    ],
                )
            )

    table = html.Div(
        className="grid",
        style={
            "gridTemplateColumns": f"repeat({COLS}, 1fr)",
        },
        children=cells,
    )

    info = [
        html.H3("Contrato físico"),
        html.P(f"Linhas: {ROWS}"),
        html.P(f"Colunas: {COLS}"),
        html.P(f"Pinos: {ROWS * COLS}"),
        html.P(f"Célula: {cell_size_cm} cm x {cell_size_cm} cm"),
        html.P(f"Mesa: {table_width_cm} cm x {table_height_cm} cm"),
        html.P("Altura dos pinos: 0 cm a 10 cm"),
        html.P("Escala de cinza futura: 0 a 255"),
        html.H3("Cantos oficiais"),
        html.P("P001 = canto superior esquerdo"),
        html.P("P016 = canto superior direito"),
        html.P("P113 = canto inferior esquerdo"),
        html.P("P128 = canto inferior direito"),
    ]

    return table, info


app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        body {
            margin: 0;
            background: #020617;
            color: #e5e7eb;
            font-family: Arial, sans-serif;
        }

        .page {
            padding: 22px;
        }

        .header {
            background: #0f172a;
            padding: 18px 22px;
            border-radius: 14px;
            margin-bottom: 16px;
            border: 1px solid #1e293b;
        }

        .header h1 {
            margin: 0 0 8px 0;
            font-size: 26px;
        }

        .controls {
            background: #0f172a;
            padding: 14px 18px;
            border-radius: 14px;
            margin-bottom: 16px;
            border: 1px solid #1e293b;
        }

        .controls label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .content {
            display: grid;
            grid-template-columns: 310px 1fr;
            gap: 18px;
        }

        .info {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 16px;
        }

        .info h3 {
            margin-top: 0;
            color: #93c5fd;
        }

        .info p {
            margin: 8px 0;
            color: #cbd5e1;
        }

        .physical-table {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 16px;
            overflow: auto;
        }

        .grid {
            display: grid;
            gap: 4px;
            min-width: 980px;
        }

        .cell {
            height: 58px;
            border: 1px solid #334155;
            border-radius: 8px;
            background: #1e293b;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #f8fafc;
        }

        .cell strong {
            font-size: 14px;
        }

        .cell span {
            font-size: 11px;
            color: #94a3b8;
            margin-top: 4px;
        }

        .corner-start {
            background: #14532d;
            border-color: #22c55e;
        }

        .corner-top-right {
            background: #1e3a8a;
            border-color: #60a5fa;
        }

        .corner-bottom-left {
            background: #713f12;
            border-color: #facc15;
        }

        .corner-end {
            background: #7f1d1d;
            border-color: #f87171;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8090)
