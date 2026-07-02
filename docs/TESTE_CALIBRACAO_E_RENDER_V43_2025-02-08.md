# TESTE CALIBRAÇÃO E RENDER — V43
Data: 08/02/2025  
Branch ativa: etapa8_integration

---

## 🎯 Objetivo do Dia

Continuar a evolução da Mesa Virtual mantendo equivalência futura com a mesa física.

Foco principal:

- ajuste fino do raster IPT (watermark)
- validação de alinhamento urbano no grid 16x8
- teste de render 2.5D (terreno + edifícios)
- preservação da arquitetura temporal existente (V41)

---

## 🧭 Trabalhos Realizados

### 1️⃣ Calibração Raster IPT

- múltiplas iterações de rotação manual
- referência visual principal:
  - Av. Escola Politécnica paralela ao eixo X
  - fachada/calçada do prédio "somatória" paralela ao eixo Y
- abordagem escolhida:
  - ajuste incremental por ângulo
  - preservação do raster original (sem destruição de resolução)

Resultado adotado:

- rotação aproximada: **-7.0°**
- watermark considerado aceitável para continuidade.

---

### 2️⃣ Bounding Box e Watermark

- geração de versões intermediárias (V47 → V54)
- identificação de problemas:

  - algumas versões consideravam a folha do desenho ao invés do urbanismo
  - perda de resolução por múltiplas rotações sucessivas

Decisão técnica:

- manter raster alinhado como referência provisória
- refinamento definitivo será feito no pipeline OFFLINE com grid maior e máscaras melhores.

---

### 3️⃣ Render Temporal V41

Estado:

✔ funcionamento preservado  
✔ fases históricas funcionando  
✔ marca d’água visível  
✔ animação temporal estável  

Observações:

- necessidade futura de refinamento do encaixe raster ↔ alturas.

---

### 4️⃣ Teste 2.5D — V43

Novo render:

render_temporal_gif_v43_terrain_building.py


Objetivo:

- separar visualmente:
  - terreno (cinza)
  - edifícios/pinos (coloridos)
- representar cotas reais em metros (Z).

Resultado:

⚠️ visual considerado estranho:

- terreno renderizado como barras verticais
- sensação de blocos empilhados
- não corresponde à percepção esperada da mesa física.

Diagnóstico:

- terreno deveria ser uma superfície contínua (mesh)
- edifícios deveriam subir sobre essa superfície.

---

## 🧠 Conclusões Técnicas do Dia

1. O modelo temporal físico continua correto.
2. O problema atual é exclusivamente visual (render 3D).
3. O raster alinhado é suficiente para continuidade.
4. Não houve regressão na arquitetura principal.

---

## 🧭 Estado Arquitetural

Pipeline ativo:

OFFLINE → CALIBRAÇÃO → RENDER → VALIDAÇÃO → GIT


Modelo mental reforçado:

- mesa virtual deve representar a mesa real futura com mínima manutenção.

---

## ⏰ Os 3 Relógios (utilizados)

1. Relógio do código → git status
2. Relógio do resultado → validação visual do render
3. Relógio do modelo físico → coerência com atuadores reais

---

## ⚠️ Observações de Arquitetura

Sinais identificados:

- mistura potencial de commits entre módulos (engine/UI/render)
- arquivos de contracts apareceram como removidos

Decisão:

- manter commits focados por camada.

---

## 🔜 Próximos Passos (Amanhã)

1. Corrigir render V43:
   - terreno como superfície contínua
   - pinos como elevação sobre o terreno.
2. Manter estética do V41.
3. Avaliar integração futura com modelo dos 3 relógios.
4. NÃO alterar pipeline offline neste momento.

---

## ⭐ Observação Estratégica

A base atual está estável.

A mesa virtual já:

- segue lógica temporal física
- possui controles interativos
- permite evolução para projeção mapeada na mesa real.

---

## ✅ Fechamento do Dia

Trabalho encerrado com:

- evolução controlada
- sem quebra do renderer canônico
- direção arquitetural preservada.
