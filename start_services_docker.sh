#!/usr/bin/env bash
set -e

cd /app

echo "Subindo IPT-CitySpace Dash em http://localhost:8050 ..."
python online/ui/dash_v128_7_28_semantic_mesa_total.py &
DASH_PID=$!

echo "Subindo Globe-CitySpace em http://localhost:8088 ..."
cd /app/globe_cityspace_open/frontend
python -m http.server 8088 &
GLOBE_PID=$!

echo ""
echo "========================================="
echo "GLOBE + IPT-CITYSPACE EM DOCKER"
echo "========================================="
echo "Globe-CitySpace : http://localhost:8088"
echo "IPT-CitySpace   : http://localhost:8050"
echo "========================================="
echo ""

trap "kill $DASH_PID $GLOBE_PID 2>/dev/null || true" EXIT

wait
