from pathlib import Path
import json
import rasterio
import pyogrio
import numpy as np

BASE = Path(__file__).resolve().parents[2]

DTM = BASE / "offline/data/processed/dtm/IPT_2018_DTM_UTM23S.tif"
ENVELOPE = BASE / "offline/products/scientific/urban_envelope_scientific.gpkg"

OUT = BASE / "offline/products/scientific/rigid_transform_utm_to_local.json"


def main():

    print("\n=== Compute UTM → LOCAL from envelope ===")

    # --- DTM bounds (UTM)
    with rasterio.open(DTM) as src:
        xmin_r, ymin_r, xmax_r, ymax_r = src.bounds

    # --- Envelope bounds (LOCAL)
    gdf = pyogrio.read_dataframe(
        ENVELOPE,
        layer="urban_envelope_scientific"
    )

    geom = gdf.geometry.iloc[0]
    xmin_e, ymin_e, xmax_e, ymax_e = geom.bounds

    # centros
    cx_r = (xmin_r + xmax_r) / 2
    cy_r = (ymin_r + ymax_r) / 2

    cx_e = (xmin_e + xmax_e) / 2
    cy_e = (ymin_e + ymax_e) / 2

    dx = cx_e - cx_r
    dy = cy_e - cy_r

    params = {
        "rotation_deg": 146.815825,  # seu valor já conhecido
        "cx": cx_r,
        "cy": cy_r,
        "tx": dx,
        "ty": dy,
        "transform_type": "utm_to_local_from_envelope"
    }

    with open(OUT, "w") as f:
        json.dump(params, f, indent=2)

    print("\nTransform computed:")
    print(json.dumps(params, indent=2))


if __name__ == "__main__":
    main()