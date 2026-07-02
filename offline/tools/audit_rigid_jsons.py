from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[2]

SEARCH_DIRS = [
    BASE / "offline",
    BASE / "offline/tools",
    BASE / "offline/validation",
    BASE / "offline/products"
]

KEYWORDS = [
    "rigid",
    "transform",
    "affine"
]


def is_relevant(path):
    name = path.name.lower()
    return any(k in name for k in KEYWORDS)


def print_json(path):
    print("\n" + "=" * 60)
    print("FILE:", path)
    print("=" * 60)

    try:
        with open(path, "r") as f:
            data = json.load(f)

        for k, v in data.items():
            print(f"{k:20} -> {v}")

    except Exception as e:
        print("ERROR:", e)


def main():

    print("\nSearching JSON files...\n")

    found = []

    for d in SEARCH_DIRS:
        if not d.exists():
            continue

        for path in d.rglob("*.json"):
            if is_relevant(path):
                found.append(path)

    if not found:
        print("No JSON files found.")
        return

    print(f"Found {len(found)} files.\n")

    for path in sorted(found):
        print_json(path)


if __name__ == "__main__":
    main()