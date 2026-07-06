#!/bin/bash

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT" || exit 1

mkdir -p _diagnosticos

echo
echo "======================================"
echo " IPT-CITYSPACE DEMO"
echo "======================================"
echo

echo "[1/4] Subindo Docker / serviços 8050 e 8088..."
docker compose up -d

echo
echo "[2/4] Ativando ambiente geo_env_2018..."
source /home/carlos/exit/etc/profile.d/conda.sh
conda activate geo_env_2018

echo
echo "[3/4] Encerrando Mesa 3D antiga, se existir..."
pkill -f dash_v129_mesa_virtual_3d_ipt.py 2>/dev/null || true

echo
echo "[4/4] Subindo Mesa Virtual 3D em 8060..."
nohup python online/ui/dash_v129_mesa_virtual_3d_ipt.py \
  > _diagnosticos/demo_mesa3d_8060.log 2>&1 &

sleep 4

echo
echo "======================================"
echo " URL PRINCIPAL DA DEMO"
echo "======================================"
echo
echo "http://localhost:8088/demo.html"
echo
echo "Serviços:"
echo "Globe-CitySpace : http://localhost:8088"
echo "IPT-CitySpace   : http://localhost:8050"
echo "Mesa 3D         : http://localhost:8060"
echo

ss -lntp | grep -E "8050|8060|8088" || true

echo
echo "Abrindo página principal..."
explorer.exe "http://localhost:8088/demo.html"
