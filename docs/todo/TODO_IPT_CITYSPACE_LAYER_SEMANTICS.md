# TODO — Semântica de Layers IPT-CitySpace

Ideia a implementar depois:

## Organização semântica
O técnico não pensa apenas em layers isoladas, mas em domínios:

- Terreno
- Edifícios
- Z Total

Cada domínio pode agrupar:

- camada de cor
- contorno / isolinhas
- cotas / valores

## Lógica operacional futura
Ao selecionar Terreno:
- ligar Terreno
- ligar Contorno Terreno, se desejado
- ligar Cotas Terreno, se desejado
- desmarcar Edifícios e Total no mesmo grupo

Ao selecionar Edifícios:
- desligar Terreno e Total no mesmo grupo

Ao selecionar Total:
- desligar Terreno e Edifícios no mesmo grupo

Grid 16x8 e Pinos/Z Total continuam independentes.

Objetivo:
melhorar a operação para técnicos acostumados com MDT, MDS, curvas de nível e isolinhas.
