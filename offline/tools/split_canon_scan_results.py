# offline/tools/split_canon_scan_results.py

"""
CitySpace – Canon Scan Splitter

Localiza automaticamente o arquivo grande "canon_scan*"
dentro do projeto e divide em pedaços pequenos.

Saída:
canon_chunks/canon_part_XXXXX.txt
"""

from pathlib import Path


# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------

ENGINE_DIR = Path("/mnt/c/IPT-CitySpace-2018/ipt-cityspace-engine")

SEARCH_ROOT = ENGINE_DIR.parent

OUTPUT_DIR = SEARCH_ROOT / "canon_chunks"

MAX_SIZE_KB = 200


# -----------------------------------------------------
# FIND INPUT FILE
# -----------------------------------------------------

def find_canon_file():

    print("Searching for canon_scan file...\n")

    for path in SEARCH_ROOT.rglob("*canon_scan*"):

        if path.is_file():

            print("Found candidate:")
            print(path)
            print()

            return path

    raise RuntimeError("No canon_scan file found")


# -----------------------------------------------------
# SPLIT
# -----------------------------------------------------

def split_file(input_file):

    OUTPUT_DIR.mkdir(exist_ok=True)

    part = 1
    size = 0

    output_path = OUTPUT_DIR / f"canon_part_{part:05d}.txt"
    out = open(output_path, "w", encoding="utf-8")

    print("Reading:", input_file)
    print("Writing to:", OUTPUT_DIR)
    print()

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            line_size = len(line.encode("utf-8"))

            if size + line_size > MAX_SIZE_KB * 1024:

                out.close()

                print("created:", output_path.name)

                part += 1
                size = 0

                output_path = OUTPUT_DIR / f"canon_part_{part:05d}.txt"
                out = open(output_path, "w", encoding="utf-8")

            out.write(line)
            size += line_size

    out.close()

    print("\nSplit completed.\n")
    print("Chunks located at:")
    print(OUTPUT_DIR)


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------

def main():

    print("\nCitySpace – Canon Scan Splitter\n")

    input_file = find_canon_file()

    split_file(input_file)


# -----------------------------------------------------

if __name__ == "__main__":
    main()