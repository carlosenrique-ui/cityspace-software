import json
from pathlib import Path
import pyogrio
import shapely
from shapely.affinity import rotate, translate

# ===================================================
# === APLICANDO TRANSFORMAÇÃO RÍGIDA (VETORES) ===
# ===================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PARAMS_PATH = BASE_DIR / "offline/products/scientific/rigid_transform_params.json"

BUILDINGS_PATH = BASE_DIR / "offline/products/scientific/buildings_scientific.gpkg"
ENVELOPE_PATH  = BASE_DIR / "offline/products/scientific/urban_envelope_scientific.gpkg"

OUT_BUILDINGS = BASE_DIR / "offline/products/scientific/buildings_scientific_rotated.gpkg"
OUT_ENVELOPE  = BASE_DIR / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"


def apply_transform(geoms, angle, cx, cy, dx, dy):
    transformed = []
    for geom in geoms:
        g = rotate(geom, angle, origin=(cx, cy), use_radians=False)
        g = translate(g, xoff=dx, yoff=dy)
        transformed.append(g)
    return transformed


def process_layer(input_path, output_path, angle, cx, cy, dx, dy):

    df = pyogrio.read_dataframe(input_path)

    geoms = df.geometry.tolist()
    new_geoms = apply_transform(geoms, angle, cx, cy, dx, dy)

    df.geometry = new_geoms

    # NÃO passar crs explicitamente
    pyogrio.write_dataframe(
        df,
        output_path,
        driver="GPKG"
    )


def main():

    print("\n===================================================")
    print("=== APLICANDO TRANSFORMAÇÃO RÍGIDA (VETORES) ===")
    print("===================================================\n")

    with open(PARAMS_PATH) as f:
        params = json.load(f)

    angle = params["theta_rotation_deg"]
    dx = params["dx"]
    dy = params["dy"]
    cx, cy = params["midpoint_original"]

    print(f"Rotação (deg): {angle}")
    print(f"Centro rotação: ({cx}, {cy})")
    print(f"Translação: dx={dx}, dy={dy}\n")

    print("Processando edifícios...")
    process_layer(BUILDINGS_PATH, OUT_BUILDINGS, angle, cx, cy, dx, dy)

    print("Processando envelope urbano...")
    process_layer(ENVELOPE_PATH, OUT_ENVELOPE, angle, cx, cy, dx, dy)

    print("\n✔ Transformação vetorial concluída com sucesso.")
    print("\nArquivos gerados:")
    print(OUT_BUILDINGS)
    print(OUT_ENVELOPE)
    print()


if __name__ == "__main__":
    main()