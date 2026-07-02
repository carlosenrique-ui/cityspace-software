#!/usr/bin/env python3
# ==========================================================
# IPT-CitySpace – CSV Product Auditor
# Verifica e compara todos os CSV gerados pelo pipeline
# ==========================================================

from pathlib import Path
import pandas as pd
import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parents[2]

SEARCH_DIRS = [
    ENGINE_ROOT / "offline/products",
    ENGINE_ROOT / "offline/products/scientific",
    ENGINE_ROOT / "offline/products/snapshots",
]

# ----------------------------------------------------------

def collect_csv():

    files = []

    for folder in SEARCH_DIRS:

        for f in folder.rglob("*.csv"):
            files.append(f)

    return sorted(files)

# ----------------------------------------------------------

def describe_csv(path):

    try:
        df = pd.read_csv(path, sep=None, engine="python")

    except Exception:
        try:
            df = pd.read_csv(path, delimiter=";")
        except Exception:
            return None

    stats = {
        "file": str(path),
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
    }

    numeric = df.select_dtypes(include=[np.number])

    if not numeric.empty:

        stats["min"] = numeric.min().min()
        stats["max"] = numeric.max().max()

    return stats

# ----------------------------------------------------------

def compare_csv(a, b):

    try:
        df1 = pd.read_csv(a, sep=None, engine="python")
        df2 = pd.read_csv(b, sep=None, engine="python")

    except Exception:
        try:
            df1 = pd.read_csv(a, delimiter=";")
            df2 = pd.read_csv(b, delimiter=";")
        except Exception:
            return False

    if df1.shape != df2.shape:
        return False

    try:
        return np.allclose(df1.values, df2.values, equal_nan=True)
    except Exception:
        return False

# ----------------------------------------------------------

def main():

    print("\n==============================================")
    print("IPT-CitySpace – CSV PRODUCT AUDIT")
    print("==============================================")

    files = collect_csv()

    print("\nCSV encontrados:", len(files))

    meta = []

    for f in files:

        stats = describe_csv(f)

        if stats:
            meta.append(stats)

            print("\nFILE:", f)
            print("rows:", stats["rows"], "cols:", stats["cols"])
            print("columns:", stats["columns"])
            if "min" in stats:
                print("range:", stats["min"], "→", stats["max"])

    print("\n----------------------------------------------")
    print("COMPARAÇÃO ENTRE CSV")
    print("----------------------------------------------")

    for i in range(len(files)):
        for j in range(i + 1, len(files)):

            if compare_csv(files[i], files[j]):

                print("\nEQUIVALENTES:")
                print(files[i])
                print(files[j])

# ----------------------------------------------------------

if __name__ == "__main__":
    main()