from pathlib import Path

ROOT = Path("/mnt/c/IPT-CitySpace-2018/ipt-cityspace-engine")

print("\nIPT-CitySpace – Altimetry Output Audit\n")

paths = [
    "offline/products",
    "offline/products/snapshots",
    "offline/products/scientific",
    "data/csv"
]

for p in paths:

    folder = ROOT / p

    print("\nChecking:", folder)

    if not folder.exists():
        print("MISSING")
        continue

    files = list(folder.rglob("*"))

    for f in files:
        if f.suffix in [".csv",".tif",".tiff"]:
            print(" ", f.relative_to(ROOT))

