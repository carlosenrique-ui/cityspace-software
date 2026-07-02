# Globe-CitySpace — Decisões Arquiteturais

## 1. Posicionamento

O Globe-CitySpace será tratado como módulo Explorer do IPT-CitySpace.

Ele não substitui o IPT-CitySpace atual.

## 2. Papel dos módulos

Globe-CitySpace:
- exploração espacial;
- navegação tipo Google Earth;
- escolha de cidade;
- escolha de ponto de referência;
- definição de escala;
- geração de área;
- geração de Grid MxN;
- geração do contrato espacial.

IPT-CitySpace:
- runtime físico;
- mesa virtual;
- mesa real;
- projeção mapeada;
- controle de atuadores;
- saídas técnicas BMP/CSV/CSD.

## 3. Tecnologia

Framework principal da plataforma:
- Dash.

Motor geoespacial 3D:
- CesiumJS.

Mapas 2D específicos:
- Leaflet / Dash-Leaflet quando necessário.

Não usar Streamlit neste momento.

## 4. Telas previstas

Tela A — Globe-CitySpace Explorer:
- Cesium;
- OSM;
- futuramente 3D Tiles;
- footprints;
- grid;
- seleção de área.

Tela B — Physical Table:
- mesa física;
- modo 1 cm;
- modo 2 cm;
- alturas 0–10 cm;
- tons de cinza;
- BMP;
- CSV;
- contrato para projeção mapeada.

Tela C — Simulation Hub:
- fora da prioridade atual;
- futuramente Mobilidade, Urbanismo e Ambiente.

## 5. Trilhas

As três trilhas do programa são:
- Mobilidade;
- Urbanismo;
- Ambiente.

Elas contribuem para o objetivo estratégico de neutralização de carbono.

Carbono não será tratado como quarta trilha neste momento.

## 6. Contratos

Separar explicitamente:

Spatial Layout:
- P001...P128;
- row;
- col;
- posição física.

Scan Layout:
- ZigZag;
- ordem de acionamento;
- ordem física/eletrônica.

Temporal Layout:
- futuro;
- evolução histórica do IPT;
- datas de construção;
- não implementar agora.

## 7. Mesa física

Contrato atual:
- 8 linhas;
- 16 colunas;
- 128 pinos;
- célula física de 1 cm ou 2 cm;
- altura máxima de 10 cm;
- tons de cinza 0–255.

## 8. Height Provider Framework

A obtenção de alturas deve ser modular.

O contrato da mesa não deve depender de uma única fonte.

Possíveis provedores:
- drone / fotogrametria;
- DSM/DTM;
- LiDAR;
- IDE municipal;
- Copernicus DEM + OSM/Microsoft/Overture;
- CityGML / 3D Tiles / BIM.

Casos:
- IPT: dados por drone/fotogrametria;
- Lisboa: IDE oficial;
- São José dos Campos: GeoSanja / IDE municipal;
- cidades com menos recursos: DEM + footprints abertos.

## 9. Altura para a mesa

A altura usada para os pinos deve seguir o conceito:

altura_total = altura_terreno + altura_edificio_estimado

Depois:
- subtrair o ponto mais baixo do grid;
- normalizar para 0–10 cm;
- converter para tons de cinza 0–255.

## 10. Saídas técnicas futuras

Para o técnico mecânico/eletrônico:
- grid_gray.bmp;
- pin_heights.csv;
- gray values;
- altura dos pinos em cm;
- ordem de acionamento;
- contratos de projeção mapeada.

## 11. 3D Tiles

3D Tiles será usado para:
- agradar o usuário/chefe;
- navegação tipo Google Earth;
- validação visual;
- exploração urbana.

Não será inicialmente a fonte principal das alturas dos pinos.

## 12. Decisão de integração

O Globe-CitySpace deverá gerar um contrato espacial que possa ser consumido pelo IPT-CitySpace.

O IPT-CitySpace permanece como base para:
- mesa virtual;
- mesa real;
- projeção mapeada;
- controle físico.
