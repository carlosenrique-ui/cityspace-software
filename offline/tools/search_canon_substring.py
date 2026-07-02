# offline/tools/search_canon_substring.py

"""
IPT-CitySpace – Canon Substring Scanner

Procura a substring "canon" em:

1) nomes de arquivos
2) conteúdo de arquivos

Saída dividida em dois arquivos para facilitar análise.

Outputs:

docs/context_snapshot/canon_scan_filenames.txt
docs/context_snapshot/canon_scan_contents.txt
"""

import os
from pathlib import Path

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------

ENGINE_ROOT = Path("/mnt/c/IPT-CitySpace-2018/ipt-cityspace-engine")

SUBSTRING = "canon"

OUT_FILENAMES = ENGINE_ROOT / "docs/context_snapshot/canon_scan_filenames.txt"
OUT_CONTENTS = ENGINE_ROOT / "docs/context_snapshot/canon_scan_contents.txt"

TEXT_EXTENSIONS = {
".py",".md",".txt",".json",".csv",".yaml",".yml",
".ini",".cfg",".geojson",".sql",".html",".js"
}

MAX_FILE_SIZE_MB = 5

# -----------------------------------------------------
# HELPERS
# -----------------------------------------------------

def is_text_file(path):
    return path.suffix.lower() in TEXT_EXTENSIONS


def file_too_big(path):
    size_mb = path.stat().st_size / (1024 * 1024)
    return size_mb > MAX_FILE_SIZE_MB


# -----------------------------------------------------
# MAIN SEARCH
# -----------------------------------------------------

def scan_tree():

    files_scanned = 0
    filename_hits = 0
    content_hits = 0

    print("\n=======================================")
    print("CitySpace – Canon Scanner")
    print("=======================================\n")

    with open(OUT_FILENAMES, "w", encoding="utf-8") as file_out, \
         open(OUT_CONTENTS, "w", encoding="utf-8") as content_out:

        file_out.write("# Canon substring in FILE NAMES\n\n")
        content_out.write("# Canon substring in FILE CONTENT\n\n")

        for root, dirs, files in os.walk(ENGINE_ROOT):

            for name in files:

                path = Path(root) / name
                files_scanned += 1

                # -----------------------------------
                # Progress indicator
                # -----------------------------------

                if files_scanned % 500 == 0:

                    print(f"Files scanned: {files_scanned}")

                # -----------------------------------
                # Filename match
                # -----------------------------------

                if SUBSTRING in name.lower():

                    file_out.write("\n-----------------------------------\n")
                    file_out.write("FILE NAME MATCH\n")
                    file_out.write("-----------------------------------\n")
                    file_out.write(str(path) + "\n")

                    filename_hits += 1

                # -----------------------------------
                # Content match
                # -----------------------------------

                if not is_text_file(path):
                    continue

                try:

                    if file_too_big(path):
                        continue

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:

                        for i, line in enumerate(f, start=1):

                            if SUBSTRING in line.lower():

                                content_out.write("\n-----------------------------------\n")
                                content_out.write("CONTENT MATCH\n")
                                content_out.write("-----------------------------------\n")
                                content_out.write(str(path) + "\n")
                                content_out.write(f"line {i}: {line.strip()}\n")

                                content_hits += 1

                except Exception:
                    pass

        # -----------------------------------
        # Summary
        # -----------------------------------

        summary = f"""

=======================================
SCAN SUMMARY
=======================================

Files scanned : {files_scanned}
Filename hits : {filename_hits}
Content hits  : {content_hits}

"""

        file_out.write(summary)
        content_out.write(summary)

    print("\nScan finished.")
    print("Results saved to:")
    print(OUT_FILENAMES)
    print(OUT_CONTENTS)


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------

def main():

    if not ENGINE_ROOT.exists():
        raise RuntimeError(f"Engine root not found: {ENGINE_ROOT}")

    OUT_FILENAMES.parent.mkdir(parents=True, exist_ok=True)

    scan_tree()


if __name__ == "__main__":
    main()