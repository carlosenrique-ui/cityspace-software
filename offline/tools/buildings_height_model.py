"""
IPT CitySpace – BUILDINGS HEIGHT MODEL
Extrai altura de edifícios usando máscaras
"""

from pathlib import Path
import numpy as np
import rasterio
from rasterio.mask import mask
import pyogrio


BASE = Path(__file__).resolve().parents[2]

HEIGHT_RASTER = BASE / "offline/data/processed/height/HEIGHT.tif"

BUILDINGS = BASE / "offline/products/scientific/buildings_scientific_rotated.gpkg"

OUTPUT = BASE / "offline/products/scientific/buildings_with_height.gpkg"


def compute_building_heights():

    print()
    print("====================================")
    print("BUILDING HEIGHT EXTRACTION")
    print("====================================")

    gdf = pyogrio.read_dataframe(BUILDINGS)

    heights_mean = []
    heights_p90 = []

    with rasterio.open(HEIGHT_RASTER) as src:

        for geom in gdf.geometry:

            out_image, _ = mask(src, [geom], crop=True)

            data = out_image[0]

            data = data[data > 0]

            if len(data) == 0:

                heights_mean.append(0)
                heights_p90.append(0)

                continue

            h_mean = float(np.mean(data))
            h_p90 = float(np.percentile(data, 90))

            heights_mean.append(h_mean)
            heights_p90.append(h_p90)

    gdf["height_mean"] = heights_mean
    gdf["height_p90"] = heights_p90

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    pyogrio.write_dataframe(
        gdf,
        OUTPUT,
        driver="GPKG"
    )

    print("Saved:", OUTPUT)

    print()
    print("Height statistics:")
    print("Mean max:", max(heights_mean))
    print("P90 max:", max(heights_p90))


def main():

    compute_building_heights()


if __name__ == "__main__":

    main()