import pyogrio
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

FILES = [
    BASE / "offline/products/scientific/buildings_scientific.gpkg",
    BASE / "offline/products/scientific/urban_envelope_scientific.gpkg",
    BASE / "offline/products/scientific/buildings_scientific_rotated.gpkg",
    BASE / "offline/products/scientific/urban_envelope_scientific_rotated.gpkg"
]

CRS_EPSG = "EPSG:31983"

for f in FILES:

    if not f.exists():
        print(f"Arquivo não encontrado: {f}")
        continue

    print(f"\nProcessando: {f.name}")

    layers = pyogrio.list_layers(f)

    for layer_name, geom_type in layers:

        print(f"  Fixando CRS na layer: {layer_name}")

        df = pyogrio.read_dataframe(f, layer=layer_name)
        df.set_crs(CRS_EPSG, inplace=True, allow_override=True)

        pyogrio.write_dataframe(
            df,
            f,
            layer=layer_name,
            driver="GPKG"
        )

print("\n✔ CRS aplicado em TODAS as layers.")