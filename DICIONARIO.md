# Dicionário de Dados — Sistema de Monitoramento de Queimadas em Minas Gerais
 
## B.1 Visão geral da base
 
| Campo | Descrição |
|---|---|
| **Título** | Sistema de monitoramento de queimadas no estado de Minas Gerais (`monitoramento_queimadas_mg`) |
| **Descrição e finalidade** | Base de dados geográficos que reúne os limites dos municípios de Minas Gerais, os focos de queimadas detectados por satélite e a delimitação dos biomas. Sua finalidade é apoiar a visualização e a análise espacial e temporal da ocorrência de focos de calor no estado, permitindo relacionar os registros aos municípios e aos biomas em que estão localizados. |
| **Fontes de dados** | **Municípios de Minas Gerais:** IBGE — Malhas Territoriais, Malha Municipal Digital (https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html; arquivos em https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/). Ano da malha: [PREENCHER].<br>**Focos de queimadas:** INPE — Programa Queimadas / Banco de Dados de Queimadas (BDQueimadas), dados de focos de calor detectados por satélite, disponibilizados em CSV (https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/).<br>**Biomas:** IBGE — base cartográfica de Biomas do Brasil (https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15842-biomas.html; arquivos em https://geoftp.ibge.gov.br/informacoes_ambientais/estudos_ambientais/biomas/vetores/). |
| **Data de coleta** | Dados de municípios e focos de queimadas: 19/11/2026. Dados de biomas: 16/11/2026. |
| **Licença** | Dados obtidos de órgãos públicos e disponibilizados para uso público. Atribuição das fontes originais e observância das condições de uso indicadas nos metadados e nas páginas de cada conjunto de dados. Recomenda-se manter junto ao projeto os metadados e os termos de uso originais. |
| **Cobertura espacial** | 853 municípios do estado de Minas Gerais, Brasil. |
| **Cobertura temporal** | Focos de queimadas registrados entre 18/11/2025 e 19/11/2026. As camadas de municípios e biomas representam recortes cartográficos de referência, não uma série histórica. |
| **SRID e justificativa** | **EPSG:4674 — SIRGAS 2000.** Sistema de referência geodésico oficial do Brasil e utilizado nas bases cartográficas do IBGE. A adoção de um único sistema de referência facilita a sobreposição e a análise espacial entre as camadas. Para medidas em metros ou quilômetros, as consultas convertem para `geography` ou reprojetam para EPSG:31983 (SIRGAS 2000 / UTM 23S). |
| **Escala e precisão** | **Municípios e biomas:** malha municipal em escala de referência 1:250.000.<br>**Focos de queimadas:** são pontos derivados de pixels de imagens de satélite; portanto, não possuem escala cartográfica única equivalente à de uma carta municipal. A resolução espacial e o erro de localização variam conforme o satélite e o sensor. O INPE informa pixels com dimensões que podem variar aproximadamente de 375 m × 375 m a 5 km × 4 km, e ressalta que a imprecisão de localização também varia conforme o sensor. |
| **Codificação e nomes** | Texto em UTF-8. Nomes de tabelas e colunas em minúsculas, sem acentos e sem espaços (snake_case). |
| **Tratamentos aplicados** | 1. Organização das camadas de municípios, biomas e focos de queimadas para utilização no QGIS.<br>2. Padronização do sistema de referência espacial para EPSG:4674 (SIRGAS 2000), verificando o SRC de origem de cada camada.<br>3. Verificação da validade das geometrias com a ferramenta **Verificar validade** (*Check validity*).<br>4. Correção das geometrias identificadas como inválidas com **Corrigir geometrias** (*Fix geometries*), quando necessário.<br>5. Verificação de registros/geometrias duplicados e remoção somente quando confirmados como duplicatas.<br>6. Preparação das camadas para importação e armazenamento no PostGIS.<br>7. Relacionamento espacial dos focos com os polígonos de municípios e biomas para preencher as chaves estrangeiras `municipio_fid` e `bioma_fid`, identificando a unidade territorial e o bioma correspondentes a cada foco. |
 
## B.2 Descrição das tabelas
 
Resumo da base: 3 tabelas espaciais (`focos_incendios`, `municipios`, `biomas`), com 2 tipos geométricos (`Point` e `MultiPolygon`), todas em SRID 4674. Total de feições: **[PREENCHER: soma dos registros das 3 tabelas]**.
 
### Tabela `focos_incendios`
 
Focos de calor detectados por satélite (INPE/BDQueimadas) em Minas Gerais. **Geometria:** Point · **SRID:** 4674 · **Registros:** [PREENCHER]
 
| Coluna | Tipo | Tam. / Domínio | Nulo? | PK / FK | Descrição | Exemplo |
|---|---|---|---|---|---|---|
| `fid` | serial (integer) | gerado | Não | PK | Identificador interno do foco. | 1 |
| `geom` | geometry | Point, 4674 | Não | | Localização do foco (centro do pixel detectado). | (geometria) |
| `datahora` | varchar | 80 · AAAA/MM/DD HH:MM:SS | Sim |  | Data e hora da detecção do foco, em texto, conforme o CSV do INPE. | 2025/11/18 00:00:00 |
| `satelite` | varchar | 100 | Sim | | Satélite/sensor que detectou o foco. | [PREENCHER] |
| `pais` | varchar | 100 | Sim | | País do foco, conforme o INPE. | [PREENCHER] |
| `estado` | varchar | 100 | Sim | | Estado do foco, conforme o INPE. | [PREENCHER] |
| `municipio` | varchar | 100 | Sim | | Nome do município do foco, conforme o INPE (texto original; ver `municipio_fid`). | [PREENCHER] |
| `bioma` | varchar | 100 | Sim | | Nome do bioma do foco, conforme o INPE (texto original; ver `bioma_fid`). | [PREENCHER] |
| `diasemchuv` | integer | 0 a 120 (nos dados) | Sim |  | Número de dias sem chuva até a detecção do foco. | [PREENCHER] |
| `precipitac` | numeric | mm · 0 a 143,18 (nos dados) | Sim |  | Precipitação acumulada no dia até o momento da detecção, em milímetros. | [PREENCHER] |
| `riscofogo` | numeric | 0 a 1 · -999 = sem valor | Sim |  | Risco de fogo previsto para o local e o dia da detecção. O valor -999 é o código do INPE para ausência de cálculo. | [PREENCHER] |
| `frp` | numeric | MW · 0 a 1974,8 (nos dados) | Sim |  | Potência radiativa do fogo (*Fire Radiative Power*), em megawatts. | [PREENCHER] |
| `latitude` | numeric | graus decimais | Sim | | Latitude do foco, conforme o CSV original. | [PREENCHER] |
| `longitude` | numeric | graus decimais | Sim | | Longitude do foco, conforme o CSV original. | [PREENCHER] |
| `bioma_fid` | bigint | ref. `biomas.fid` | Sim | FK | Bioma em que o foco se localiza. Referencia `biomas.fid`. | [PREENCHER] |
| `municipio_fid` | bigint | ref. `municipios.fid` | Sim | FK | Município em que o foco se localiza. Referencia `municipios.fid`. | [PREENCHER] |
 
### Tabela `municipios`
 
Limites dos municípios de Minas Gerais (IBGE, Malha Municipal Digital). **Geometria:** MultiPolygon · **SRID:** 4674 · **Registros:** [PREENCHER: esperado 853]
 
| Coluna | Tipo | Tam. / Domínio | Nulo? | PK / FK | Descrição | Exemplo |
|---|---|---|---|---|---|---|
| `fid` | serial (integer) | gerado | Não | PK | Identificador interno do município nesta base. | 461 |
| `geom` | geometry | MultiPolygon, 4674 | Não | | Limite municipal. | (geometria) |
| `cd_mun` | varchar | 7 dígitos · único | Não | | Código do município no IBGE. | 3106200 |
| `nm_mun` | varchar | 100 | Não | | Nome do município. | Belo Horizonte |
| `cd_rgi` | varchar | 6 | Sim |  | Código da Região Geográfica Imediata. | 310001 |
| `nm_rgi` | varchar | 100 | Sim |  | Nome da Região Geográfica Imediata. | Belo Horizonte |
| `cd_rgint` | varchar | 4 | Sim |  | Código da Região Geográfica Intermediária. | 3101 |
| `nm_rgint` | varchar | 100 | Sim |  | Nome da Região Geográfica Intermediária. | Belo Horizonte |
| `cd_uf` | varchar | 2 | Sim | | Código da unidade da federação no IBGE (31 = Minas Gerais). | 31 |
| `nm_uf` | varchar | 50 | Sim | | Nome da unidade da federação. | Minas Gerais |
| `sigla_uf` | varchar | 2 | Sim | | Sigla da unidade da federação. | MG |
| `cd_regiao` | varchar | 1 | Sim | | Código da Grande Região (3 = Sudeste). | 3 |
| `nm_regiao` | varchar | 20 | Sim | | Nome da Grande Região. | Sudeste |
| `sigla_rg` | varchar | 2 | Sim | | Sigla da Grande Região. | SE |
| `cd_concurb` | varchar | 7 | Sim |  | Código da Concentração Urbana (nulo se o município não pertence a uma). | 3106200 |
| `nm_concurb` | varchar | 100 | Sim |  | Nome da Concentração Urbana. | Belo Horizonte/MG |
| `area_km2` | double precision | ≥ 0 · km² | Sim |  | Área territorial em km², conforme a malha do IBGE. | 331.337 |
 
### Tabela `biomas`
 
Limites dos seis biomas brasileiros (IBGE, Biomas do Brasil), em recorte nacional: a camada não foi cortada para Minas Gerais. **Geometria:** MultiPolygon · **SRID:** 4674 · **Registros:** 6
 
| Coluna | Tipo | Tam. / Domínio | Nulo? | PK / FK | Descrição | Exemplo |
|---|---|---|---|---|---|---|
| `fid` | serial (integer) | gerado | Não | PK | Identificador interno do bioma nesta base. | 1 |
| `geom` | geometry | MultiPolygon, 4674 | Não | | Limite do bioma. | (geometria) |
| `cd_bioma` | varchar | 1 · único | Não |  | Código do bioma no IBGE. | 1 |
| `nm_bioma` | varchar | 100 | Não |  | Nome do bioma. | Amazônia |
| `area_km2` | numeric | (14,3) · ≥ 0 · km² | Sim |  | Área do bioma em km², calculada com `ST_Area` sobre `geography`. | 4215443.665 |
 
## B.3 Relacionamentos
 
| Origem | Destino | Tipo | Descrição |
|---|---|---|---|
| `focos_incendios.municipio_fid` | `municipios.fid` | FK 1:N | Cada foco pertence a um município; um município tem vários focos. |
| `focos_incendios.bioma_fid` | `biomas.fid` | FK 1:N | Cada foco pertence a um bioma; um bioma tem vários focos. |
| `focos_incendios.geom` | `municipios.geom` | Espacial | `ST_Within(focos_incendios.geom, municipios.geom)`: o ponto está contido no município; usada para validar `municipio_fid`. |
| `focos_incendios.geom` | `biomas.geom` | Espacial | `ST_Within(focos_incendios.geom, biomas.geom)`: o ponto está contido no bioma; usada para validar `bioma_fid`. |
| `municipios.geom` | `biomas.geom` | Espacial N:N | `ST_Intersects`: um município pode ocupar mais de um bioma, e um bioma abrange vários municípios. |
 
## B.4 Domínios e códigos
 
| Coluna | Valor | Significado |
|---|---|---|
| `municipios.cd_uf` | 31 | Minas Gerais |
| `municipios.cd_regiao` | 3 | Sudeste |
| `municipios.sigla_rg` | SE | Sudeste |
| `biomas.cd_bioma` | 1 | Amazônia |
| | 2 | Caatinga |
| | 3 | Cerrado |
| | 4 | Mata Atlântica |
| | 5 | Pampa |
| | 6 | Pantanal |
| `focos_incendios.riscofogo` | -999 | Sem valor calculado (código do INPE) |
| | 0 a 1 | Risco de fogo previsto |
| `focos_incendios.satelite` | [PREENCHER: valores distintos] | [PREENCHER] |
 
## B.5 Qualidade e limitações
 
- **Foco de calor não é queimada confirmada:** cada ponto indica a detecção de calor em um pixel de imagem de satélite; um mesmo incêndio pode gerar vários focos, e queimadas pequenas ou curtas podem não ser detectadas.
- **Precisão posicional:** a localização do foco é a do pixel, com erro que varia conforme o satélite e o sensor (de centenas de metros a alguns quilômetros).
- **Nomes de município e bioma em texto:** `focos_incendios.municipio` e `focos_incendios.bioma` vêm do INPE e podem divergir da grafia ou do limite das tabelas `municipios` e `biomas`; para análises, prefira os campos `municipio_fid` e `bioma_fid`.
- **Focos sem vínculo:** 104.744 focos têm `municipio_fid` ou `bioma_fid` nulo, por não terem sido associados a um polígono das tabelas `municipios` ou `biomas`. [PREENCHER: total de focos e causa, ex.: focos fora de Minas Gerais]
- **Geometrias:** nas três tabelas, 0 geometrias inválidas (`ST_IsValid`).
- **Valores ausentes:** `riscofogo` usa -999 para ausência de valor (convenção do INPE); ao calcular médias, filtre `riscofogo >= 0`. Faixas observadas: `diasemchuv` de 0 a 120, `precipitac` de 0 a 143,18 mm, `frp` de 0 a 1974,8 MW.
- **Biomas em escala nacional:** a tabela `biomas` contém os 6 biomas do Brasil e a `area_km2` é a do bioma inteiro, não só da parte em Minas Gerais.
- **Escala:** os limites municipais e de biomas (1:250.000) servem para análises regionais, não para análises cadastrais. Focos próximos à divisa podem ser atribuídos ao município ou bioma vizinho.
- **Temporalidade:** retrato de 18/11/2025 a 19/11/2026. O BDQueimadas é atualizado continuamente pelo INPE.
 