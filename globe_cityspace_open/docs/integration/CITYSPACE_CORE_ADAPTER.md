# CitySpace Core Adapter

## Objetivo

Evitar que o Globe-CitySpace vire uma teia de aranha de chamadas diretas para os módulos antigos `offline/` e `online/`.

## Regra principal

Globe-CitySpace não importa diretamente módulos legados do IPT-CitySpace.

Em vez disso:

Globe-CitySpace Explorer
↓
spatial_project.json
↓
CitySpace Core Adapter
↓
IPT-CitySpace Runtime

## Papel do Globe-CitySpace

Produzir contratos espaciais:

- cidade;
- ponto de referência;
- escala;
- grid;
- spatial layout;
- projeto espacial.

## Papel do IPT-CitySpace

Consumir contratos e produzir:

- alturas;
- normalização 0–10 cm;
- BMP;
- CSV;
- actuator_plan.json;
- mesa virtual;
- mesa real;
- projeção mapeada.

## Decisão

Os pipelines rodam em paralelo, mas se comunicam por contratos.

Não há acoplamento direto entre o Explorer e os módulos antigos.
