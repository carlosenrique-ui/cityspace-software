"""
IPT-CitySpace
AUDIT + AUTO FIX

Objetivo
--------

Encontrar e corrigir automaticamente:

    set_height_cm  -> set_height_cm

e eventos:

    "value" -> "value_cm"

Somente em arquivos Python.

Gera relatórios em:

docs/architecture/code_audit/

Uso:

python offline/tools/audit_fix_set_pin.py
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = ROOT / "docs/architecture/code_audit"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FOUND = REPORT_DIR / "audit_set_pin_found.txt"
REPORT_FIXED = REPORT_DIR / "audit_set_pin_fixed.txt"


EXCLUDE_DIRS = {
    "docs",
    "__pycache__",
    ".git",
    "legacy"
}


def should_skip(path: Path):

    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True

    return False


def find_python_files():

    files = []

    for p in ROOT.rglob("*.py"):

        if should_skip(p):
            continue

        files.append(p)

    return files


def audit_files(files):

    found = []

    for f in files:

        text = f.read_text(encoding="utf-8")

        if "set_height_cm" in text:

            found.append(f)

    return found


def fix_file(path: Path):

    text = path.read_text(encoding="utf-8")

    original = text

    text = re.sub(
        r"\bset_pin\b",
        "set_height_cm",
        text
    )

    text = re.sub(
        r'"value_cm":',
        '"value_cm":',
        text
    )

    if text != original:

        path.write_text(text, encoding="utf-8")

        return True

    return False


def main():

    print("\n================================")
    print("IPT CitySpace – set_height_cm AUDIT")
    print("================================\n")

    files = find_python_files()

    print(f"Python files scanned: {len(files)}")

    found = audit_files(files)

    print(f"Files containing set_height_cm: {len(found)}")

    REPORT_FOUND.write_text(
        "\n".join(str(f) for f in found),
        encoding="utf-8"
    )

    fixed = []

    for f in found:

        changed = fix_file(f)

        if changed:
            fixed.append(f)

    REPORT_FIXED.write_text(
        "\n".join(str(f) for f in fixed),
        encoding="utf-8"
    )

    print("\nFiles fixed:", len(fixed))

    print("\nReport files:")
    print(REPORT_FOUND)
    print(REPORT_FIXED)

    print("\n================================")
    print("AUDIT COMPLETE")
    print("================================\n")


if __name__ == "__main__":
    main()