# Height Provider Framework

## Objetivo

O Height Provider Framework define como o IPT-CitySpace / Globe-CitySpace poderá obter alturas para alimentar a mesa virtual, a mesa real, BMPs, CSVs e projeção mapeada.

A arquitetura deve permitir múltiplas fontes de dados, pois cada cidade pode ter diferentes níveis de maturidade geoespacial.

## Contrato de saída

Independentemente da fonte, o resultado deve produzir:

- cell_id;
- terrain_height_m;
- building_height_m;
- total_height_m;
- relative_height_m;
- pin_height_cm;
- gray_value.

## Fórmula base

total_height_m = terrain_height_m + building_height_m

relative_height_m = total_height_m - min(total_height_m no grid)

pin_height_cm = normalização de relative_height_m para 0–10 cm

gray_value = normalização de pin_height_cm para 0–255

## Providers previstos

### 1. Estimated DEM + Footprints Provider

Uso:
- cidades com poucos recursos;
- MVP;
- baixo custo.

Fontes:
- Copernicus DEM;
- OSM Buildings;
- Microsoft Building Footprints;
- Overture Maps.

### 2. Drone / Photogrammetry Provider

Uso:
- IPT;
- áreas levantadas por drone.

Fontes:
- DSM;
- DTM;
- ortofotos;
- produtos fotogramétricos.

### 3. DSM / DTM Provider

Uso:
- cidades com modelos oficiais de superfície e terreno.

Fontes:
- MDS;
- MDT;
- dados municipais.

### 4. LiDAR Provider

Uso:
- maior precisão científica.

Fontes:
- LAS;
- LAZ;
- nuvem de pontos classificada.

### 5. Municipal IDE Provider

Uso:
- cidades com infraestrutura oficial de dados espaciais.

Exemplos:
- Lisboa;
- São José dos Campos / GeoSanja;
- outras IDEs municipais.

### 6. City Digital Twin Provider

Uso futuro:
- CityGML;
- 3D Tiles;
- BIM;
- digital twins municipais.

## Casos do projeto Cidades Carbono Neutro

### IPT

Provider provável:
- drone / fotogrametria;
- DSM/DTM local.

### São José dos Campos

Provider provável:
- GeoSanja / IDE municipal;
- eventual complemento com DEM + footprints.

### Santos

Provider provável:
- dados municipais quando disponíveis;
- complemento com DEM + footprints.

### Sorocaba

Provider provável:
- DEM + OSM/Microsoft/Overture;
- dados municipais se disponíveis.

## Princípio arquitetural

A mesa física não deve depender da origem dos dados.

Apenas o Height Provider muda.

O contrato final de alturas permanece estável.
