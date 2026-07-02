#!/usr/bin/env bash
set -e

cd /mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean

eval "$(conda shell.bash hook)"
conda activate geo_env_2018

echo "Subindo IPT-CitySpace Dash em http://localhost:8050 ..."
python online/ui/dash_v128_7_20_work_from_719.py &
DASH_PID=$!

echo "Subindo Globe-CitySpace em http://localhost:8088 ..."
cd globe_cityspace_open/frontend
python -m http.server 8088 &
GLOBE_PID=$!

echo ""
echo "========================================="
echo "Globe-CitySpace integrado iniciado"
echo "========================================="
echo "Globe-CitySpace : http://localhost:8088"
echo "IPT-CitySpace   : http://localhost:8050"
echo "Mapping Project : abre http://localhost:8050"
echo "========================================="
echo "Para parar: CTRL+C"
echo ""

trap "kill $DASH_PID $GLOBE_PID 2>/dev/null || true" EXIT

wait
