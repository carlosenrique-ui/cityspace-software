# CitySpace Core Reuse Map

## Objetivo

Mapear quais componentes já existentes do IPT-CitySpace serão reaproveitados pelo Globe-CitySpace, evitando duplicação de código e evitando que os pipelines virem uma teia de aranha.

## Regra Arquitetural

O Globe-CitySpace não deve importar diretamente módulos antigos `offline/` e `online/`.

O fluxo deve ser:

Globe-CitySpace Explorer
↓
spatial_project.json
↓
CitySpace Core Adapter
↓
IPT-CitySpace Runtime

---

## Componentes Reaproveitáveis

### 1. Controle Temporal

Arquivos candidatos:

- `online/core/temporal_core_directional.py`
- `online/core/temporal_player.py`
- `online/runtime/plan_player.py`

Funções/conceitos existentes:

- play_forward
- play_backward
- pause
- reset
- tick
- step_forward
- step_backward

Uso futuro:

- Mesa Virtual
- Mesa Real
- Projeção Mapeada
- Timeline histórica futura do IPT

Status:

Reaproveitar com adaptação controlada via Adapter.

---

### 2. ZigZag / Scan Pattern

Arquivos candidatos:

- `online/renderers/render_mesa_ipt_zigzag_integrada_final.py`
- `online/renderers/render_mesa_ipt_zigzag_canonico.py`
- `online/renderers/render_mesa_ipt_animacao_zigzag.py`

Funções/conceitos existentes:

- ordem_zigzag
- build_zigzag_path
- animação por ordem física
- renderização da mesa

Status:

Reaproveitar como referência canônica, mas manter separado do Spatial Layout.

Decisão importante:

Spatial Layout ≠ Scan Layout

O Spatial Layout define P001...P128.
O Scan Layout define a ordem de acionamento.

---

### 3. Height Engine

Arquivos candidatos:

- `offline/processing/compute_heights.py`
- `offline/tools/buildings_height_model.py`
- `offline/grid_to_pin_height.py`

Funções/conceitos existentes:

- compute_heights
- compute_building_heights
- grid_to_pin_height
- geração de actuator_plan

Uso futuro:

- Height Provider Framework
- altura do terreno
- altura de edifício
- altura total
- normalização 0–10 cm
- tons de cinza 0–255

Status:

Reaproveitar com abstração por Height Provider.

---

### 4. Actuator Plan

Arquivos candidatos:

- `offline/grid_to_pin_height.py`
- `offline/pipeline/04_generate_actuator_plan.py`
- `offline/pipeline/04b_generate_actuator_geospatial.py`
- `online/runtime/plan_player.py`

Artefatos existentes:

- `actuator_plan.json`
- eventos `set_height_cm`

Uso futuro:

- Mesa Real
- testes com técnico mecânico/eletrônico
- sincronização com Mesa Virtual

Status:

Reaproveitar via contrato, não por importação direta espalhada.

---

### 5. Projection Mapping

Arquivos candidatos:

- `online/ui/dash_v112_true_align_projection_ready.py`
- `online/ui/dash_v114_watermark_calibrator_projection.py`
- `online/ui/dash_v115_projection_baseline.py`
- `online/ui/dash_v96_watermark_calibrator.py`
- `offline/tools/generate_grid_aligned_watermark.py`
- `offline/tools/generate_grid_aligned_watermark_v2.py`

Uso futuro:

- projeção mapeada 1 cm x 1 cm
- projeção mapeada 2 cm x 2 cm
- alinhamento com mesa física
- validação visual do grid

Status:

Reaproveitar como módulo separado de Projection Mapping.

---

## Componentes do Globe-CitySpace

### Explorer

Responsável por:

- navegação Cesium;
- cidade;
- ponto de referência;
- escala;
- área;
- grid;
- spatial_project.json.

Não deve ser responsável por:

- controle de atuadores;
- projeção mapeada;
- normalização final;
- runtime físico.

---

### CitySpace Core Adapter

Responsável por:

- validar contratos;
- conectar o projeto espacial ao runtime IPT-CitySpace;
- manter fronteiras entre pipelines.

---

## Pipelines

### Pipeline A — Globe-CitySpace

Entrada:

- cidade;
- lat/lon;
- escala;
- grid;
- seleção espacial.

Saída:

- `spatial_project.json`

---

### Pipeline B — IPT-CitySpace

Entrada:

- `spatial_project.json`
- contratos físicos;
- dados de altura;
- dados de projeção.

Saída:

- height contract;
- BMP;
- CSV;
- actuator plan;
- mesa virtual;
- mesa real;
- projeção mapeada.

---

## Decisão

Os pipelines rodam em paralelo, mas só se comunicam por contratos.

Não haverá acoplamento direto entre Explorer e módulos legados.

---

## Próximos Passos

1. Gerar `spatial_project.json` automaticamente a partir do Explorer.
2. Criar `height_contract.json`.
3. Adaptar Height Provider Framework.
4. Reaproveitar geração de actuator plan.
5. Reaproveitar Projection Mapping.
6. Integrar Mesa Virtual e Mesa Real via CitySpace Core Adapter.
