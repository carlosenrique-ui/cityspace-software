"""
IPT CitySpace
AUTO FIX – SCIENTIFIC RASTER RUNNER ENVELOPE

Corrige automaticamente:

geom = shape(shp[0]["geometry"])

para

geom = load_envelope_geometry()

e adiciona a função load_envelope_geometry()

Arquivo alvo:
offline/raster/pipeline/scientific_raster_runner.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TARGET = ROOT / "offline/raster/pipeline/scientific_raster_runner.py"

REPORT = ROOT / "docs/architecture/code_audit/raster_runner_envelope_fix.txt"


FUNCTION = """

def load_envelope_geometry():

    import geopandas as gpd

    print("\\n[ENVELOPE] carregando envelope científico rotacionado clean")

    gdf = gpd.read_file(
        ENVELOPE,
        layer="urban_envelope_scientific_rotated_clean"
    )

    if gdf.empty:
        raise RuntimeError(
            "Envelope científico vazio – verifique o GPKG"
        )

    geom = gdf.geometry.iloc[0]

    print("Envelope bounds:", geom.bounds)

    return geom

"""


def main():

    print("\n========================================")
    print("IPT CitySpace – FIX SCIENTIFIC RUNNER")
    print("========================================\n")

    text = TARGET.read_text()

    replaced = False

    if "shape(shp[0]" in text:

        text = text.replace(
            "geom = shape(shp[0][\"geometry\"])",
            "geom = load_envelope_geometry()"
        )

        replaced = True

    if "def load_envelope_geometry" not in text:

        text = FUNCTION + "\n\n" + text

    TARGET.write_text(text)

    REPORT.write_text(
        f"Arquivo corrigido: {TARGET}\nReplaced geom line: {replaced}\n"
    )

    print("Arquivo corrigido:", TARGET)
    print("Relatório:", REPORT)

    print("\n========================================")
    print("FIX COMPLETE")
    print("========================================\n")


if __name__ == "__main__":
    main()