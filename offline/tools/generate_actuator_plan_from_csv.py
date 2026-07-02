from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[2]

CSV = BASE / "offline/products/grid_z_total_m.csv"
OUT = BASE / "offline/products/actuator_plan.json"


def main():

    print("\n=== GENERATE ACTUATOR PLAN (MATRIX) ===\n")

    if not CSV.exists():
        raise FileNotFoundError(CSV)

    plan = []

    with open(CSV) as f:
        lines = f.readlines()

    grid_rows = len(lines)
    grid_cols = None

    for i, line in enumerate(lines):

        values = line.strip().split(";")

        if grid_cols is None:
            grid_cols = len(values)

        for j, val in enumerate(values):

            val = val.replace(",", ".").strip()

            if val == "":
                z = 0.0
            else:
                z = float(val)

            plan.append({
                "row": i,
                "col": j,
                "z": z
            })

    output = {
        "grid_rows": grid_rows,
        "grid_cols": grid_cols,
        "actuators": plan
    }

    with open(OUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Grid: {grid_rows} x {grid_cols}")
    print("Saved:", OUT)


if __name__ == "__main__":
    main()