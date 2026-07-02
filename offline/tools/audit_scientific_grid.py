from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

print("\nIPT-CitySpace – Scientific Grid Audit\n")

path = ROOT / "offline/products/scientific/grid_metrics_utm.csv"

if not path.exists():
    print("ERRO: arquivo não encontrado")
    print(path)
    exit()

df = pd.read_csv(path)

print("Arquivo:", path)

print("\nTotal de linhas:", len(df))

print("\nColunas:")
for c in df.columns:
    print(" ", c)

if "z_total_m" in df.columns:

    print("\nEstatísticas de z_total_m\n")
    print(df["z_total_m"].describe())

else:
    print("\nColuna z_total_m não encontrada")

print("\nAudit finalizado\n")