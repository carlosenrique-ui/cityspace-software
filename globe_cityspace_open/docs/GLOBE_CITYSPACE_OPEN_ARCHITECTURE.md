# Globe-CitySpace Open Architecture

O Globe-CitySpace Open é um pipeline paralelo ao IPT-CitySpace atual.

Ele não altera os módulos offline/online existentes.

## Arquitetura

CesiumJS + OpenStreetMap + edifícios abertos + DEM gratuito
↓
seleção de área
↓
grid 16x8
↓
128 alturas
↓
mesa virtual

## Princípio

O sistema deve permanecer isolado até validação do MVP.
