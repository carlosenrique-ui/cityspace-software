"""
IPT-CitySpace
List all raster files (DTM / DSM)
"""

from pathlib import Path


BASE = Path(__file__).resolve().parents[2]


def main():

    print("\n==========================================")
    print("Searching for DTM / DSM rasters")
    print("==========================================\n")

    exts = [".tif", ".tiff"]

    for path in BASE.rglob("*"):
        if path.suffix.lower() in exts:

            name = path.name.lower()

            if "dtm" in name or "dsm" in name:
                print(path)

    print("\nDone.\n")


if __name__ == "__main__":
    main()