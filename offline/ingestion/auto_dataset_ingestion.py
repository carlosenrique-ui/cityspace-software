"""
IPT-CitySpace
AUTOMATED DATA INGESTION + PIPELINE START

Fluxo automático:

ZIP (cliente)
↓
unzip
↓
detectar DSM / DTM
↓
padronizar nomes
↓
mover para RAW
↓
disparar pipeline científico

Autor: Carlos Enrique / IPT
"""

import zipfile
import shutil
import subprocess
from pathlib import Path

print("\n================================================")
print("IPT-CitySpace – AUTOMATED DATA INGESTION")
print("================================================\n")

BASE = Path(__file__).resolve().parents[2]

INCOMING = BASE / "offline/data/incoming"
RAW = BASE / "offline/data/raw"
TEMP = BASE / "offline/data/_temp_ingestion"

print("BASE:", BASE)

print("\n[1] Garantindo estrutura de diretórios...\n")

INCOMING.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
TEMP.mkdir(parents=True, exist_ok=True)

print("INCOMING:", INCOMING)
print("RAW:", RAW)

print("\n[2] Procurando ZIP do cliente...\n")

zip_files = list(INCOMING.glob("*.zip"))

if not zip_files:
    print("Nenhum ZIP encontrado em:", INCOMING)
    print("Coloque o dataset do cliente nessa pasta.")
    exit()

zip_file = zip_files[0]

print("ZIP detectado:", zip_file)

print("\n[3] Extraindo dataset...\n")

with zipfile.ZipFile(zip_file, 'r') as z:
    z.extractall(TEMP)

print("Extraído para:", TEMP)

print("\n[4] Procurando rasters DSM / DTM...\n")

tif_files = list(TEMP.rglob("*.tif"))

DSM = None
DTM = None

for f in tif_files:

    name = f.name.lower()

    if "dtm" in name:
        DTM = f

    if "dsm" in name or "dem" in name or "elevation" in name:
        DSM = f

        print("DSM detectado:", DSM)
        print("DTM detectado:", DTM)

    if DSM is None or DTM is None:
        print("\nERRO: DSM ou DTM não identificados.")
        print("\nArquivos TIFF encontrados:\n")

    for t in tif_files:
        print(" -", t)

exit()

print("\n[5] Padronizando nomes científicos...\n")

DSM_TARGET = RAW / "IPT-2018-DSM.tif"
DTM_TARGET = RAW / "IPT-2018-DTM.tif"

print("Destino DSM:", DSM_TARGET)
print("Destino DTM:", DTM_TARGET)

print("\n[6] Copiando arquivos para RAW...\n")

shutil.copy(DSM, DSM_TARGET)
shutil.copy(DTM, DTM_TARGET)

print("✔ DSM copiado")
print("✔ DTM copiado")

print("\n[7] Limpando pasta temporária...\n")

shutil.rmtree(TEMP)

print("TEMP removido")

print("\n[8] Iniciando pipeline científico raster...\n")

cmd = [
"python",
"-m",
"offline.raster.pipeline.scientific_raster_runner"
]

subprocess.run(cmd)

print("\n================================================")
print("PIPELINE COMPLETO FINALIZADO")
print("================================================\n")
