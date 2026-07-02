# Workflow Develooment Method usning chaGPT AI
## IPT-CitySpace Development Protocol

Este documento define **como trabalhar de forma produtiva no projeto IPT-CitySpace**.

Ele estabelece o método preferido de desenvolvimento utilizado por Carlos Henrique Simoes.

O objetivo é evitar:

- erros humanos
- instruções incompletas
- soluções não executáveis
- perda de contexto entre chats

---

# 1. PRINCÍPIO FUNDAMENTAL

Sempre entregar **SOLUÇÕES PRONTAS**.

Nunca entregar apenas:

- sugestões
- ideias
- trechos incompletos
- instruções ambíguas

Toda resposta deve permitir:


copiar
colar
executar


---

# 2. FORMATO PADRÃO DE ENTREGA

Toda solução deve conter:

1️⃣ Arquivo completo quando houver código  
2️⃣ Caminho do arquivo  
3️⃣ Bash agrupado para execução  
4️⃣ Sem comandos interativos

---

# 3. PROIBIDO NO WORKFLOW

Evitar completamente:


nano
vim
cat
python - <<'PY'


Esses comandos aumentam o risco de erro humano.

---

# 4. EXECUÇÃO DE SCRIPTS

Sempre executar scripts usando:


python -m module.path


Nunca:


python script.py


Isso garante:

- consistência de ambiente
- execução dentro do pacote
- melhor manutenção do projeto

---

# 5. BASH AGRUPADO

Sempre fornecer comandos agrupados.

Exemplo:


cd /mnt/c/IPT-CitySpace-2018/ipt-cityspace-engine

conda activate geo_env_2018

python -m offline.scientific_cell_metrics_utm

python -m offline.adapters.scientific_to_semantic_adapter


Isso permite execução direta sem edição manual.

---

# 6. SEM ALTERAÇÃO DESNECESSÁRIA DE ARQUITETURA

Evitar:

- criar novas variáveis
- criar novos diretórios
- mudar nomes de arquivos
- alterar estrutura do pipeline

A menos que seja **estritamente necessário**.

Priorizar **reuso do código existente**.

---

# 7. RESPEITAR A ARQUITETURA DO PROJETO

Arquitetura oficial:


OFFLINE
↓
SCIENTIFIC PIPELINE
↓
SEMANTIC ADAPTER
↓
ONLINE RUNTIME
↓
UI / MESA VIRTUAL
↓
MESA FÍSICA


Regras importantes:

- UTM existe apenas no **offline**
- runtime usa **grid da mesa**
- UI trabalha com **row / col**

---

# 8. DETECÇÃO AUTOMÁTICA DE ERROS

Sempre que possível criar:

- scripts de auditoria
- validações automáticas
- testes de integridade

Exemplos:


audit_alignment_grid_raster
audit_scientific_grid
validate_pipeline_products


---

# 9. OBJETIVO DO PROJETO

O sistema IPT-CitySpace deve produzir:


mesa física de pinos
+
projeção mapeada
+
modelo digital sincronizado


Arquitetura inspirada em:

- MIT Tangible Media Lab
- Tangible Landscape (NC State)

---

# 10. FILOSOFIA DE DESENVOLVIMENTO

O foco é:


robustez
reprodutibilidade
pipeline científico confiável


Evitar improvisos e preferir:


engenharia de sistema


---

# 11. PRINCÍPIO FINAL

A regra mais importante:


ENTREGAR SOLUÇÃO PRONTA


Não apenas explicação.

O objetivo é permitir que o sistema avance rapidamente
sem necessidade de reinterpretação das instruções.
✔ Isso resolve um problema real

Esse documento garante que:

cada nova conversa segue o mesmo método

não voltamos a problemas de comunicação

o projeto continua com ritmo de engenharia
