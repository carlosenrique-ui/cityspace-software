from pathlib import Path

print("\n=================================================")
print("IPT-CitySpace – FIX VALIDATION SCRIPTS")
print("=================================================\n")

BASE = Path(__file__).resolve().parents[2]

TARGET_FILE = BASE / "offline/validation/validate_rotated_raster_vs_envelope.py"

print("Arquivo alvo:")
print(TARGET_FILE)

if not TARGET_FILE.exists():
raise FileNotFoundError("Arquivo não encontrado.")

print("\nLendo conteúdo...")

text = TARGET_FILE.read_text()

print("Aplicando correções automáticas...")

text = text.replace("**file**", "**file**")
text = text.replace("", "")

TARGET_FILE.write_text(text)

print("\n✔ Correção aplicada com sucesso.")
print("Agora o script pode ser executado normalmente.\n")
