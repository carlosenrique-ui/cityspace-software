"""
IPT CitySpace
ENVELOPE PIPELINE AUDIT + FIX

Objetivo
--------

Padronizar o pipeline para usar:

urban_envelope_scientific_rotated_clean.gpkg

em vez de

urban_envelope_scientific_rotated_clean.gpkg

Somente nos módulos que CONSOMEM o envelope.

Relatórios gerados:

docs/architecture/code_audit/envelope_audit_found.txt
docs/architecture/code_audit/envelope_audit_fixed.txt
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = ROOT / "docs/architecture/code_audit"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FOUND = REPORT_DIR / "envelope_audit_found.txt"
REPORT_FIXED = REPORT_DIR / "envelope_audit_fixed.txt"

OLD = "urban_envelope_scientific_rotated_clean.gpkg"
NEW = "urban_envelope_scientific_rotated_clean.gpkg"

EXCLUDE = [
    "build_official_urban_envelope_rotated.py",
    "apply_rigid_transform_vector_scientific.py",
    "set_crs_scientific.py"
]


def scan_files():

    results = []

    for f in ROOT.rglob("*.py"):

        if "__pycache__" in str(f):
            continue

        text = f.read_text(encoding="utf-8")

        if OLD in text:
            results.append(f)

    return results


def fix_file(path):

    if any(x in str(path) for x in EXCLUDE):
        return False

    text = path.read_text(encoding="utf-8")

    new_text = text.replace(OLD, NEW)

    if new_text != text:

        path.write_text(new_text, encoding="utf-8")

        return True

    return False


def main():

    print("\n====================================")
    print("IPT CitySpace – ENVELOPE AUDIT")
    print("====================================\n")

    files = scan_files()

    REPORT_FOUND.write_text(
        "\n".join(str(f) for f in files),
        encoding="utf-8"
    )

    print("Files referencing rotated envelope:", len(files))

    fixed = []

    for f in files:

        if fix_file(f):
            fixed.append(f)

    REPORT_FIXED.write_text(
        "\n".join(str(f) for f in fixed),
        encoding="utf-8"
    )

    print("Files corrected:", len(fixed))

    print("\nReports generated:")
    print(REPORT_FOUND)
    print(REPORT_FIXED)

    print("\n====================================")
    print("AUDIT COMPLETE")
    print("====================================\n")


if __name__ == "__main__":
    main()