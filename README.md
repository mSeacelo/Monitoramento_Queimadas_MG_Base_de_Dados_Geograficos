# Monitoramento de Queimadas em Minas Gerais — Base de Dados Geográficos

Exercício "Coleta e Documentação de uma Base de Dados Geográficos" (CSI803 – Banco de Dados Geográficos, UFOP, Prof. Bruno R. Monteiro).

## Descrição

Base geográfica no PostGIS com os municípios de Minas Gerais, os biomas e os focos de calor detectados por satélite entre 18/11/2025 e 19/11/2026. Serve para analisar onde e quando ocorrem focos de queimadas e a que município e bioma pertencem.

- 3 tabelas espaciais: `focos_incendios` (Point), `municipios` (MultiPolygon), `biomas` (MultiPolygon)
- SRID: 4674 (SIRGAS 2000)
- Total de feições: [PREENCHER]
- Modelo e diagramas: pasta `Artefatos/`
- Dicionário de dados completo: [DICIONÁRIO.md](DICION%C3%81RIO.md)

## Fontes e licença dos dados

| Dado | Fonte | Coleta | Licença |
|---|---|---|---|
| Municípios | IBGE — Malha Municipal Digital. Portal: <https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html> · Arquivos: <https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/> | 19/11/2026 | Dados abertos; citar o IBGE |
| Biomas | IBGE — Biomas do Brasil. Portal: <https://www.ibge.gov.br/geociencias/informacoes-ambientais/estudos-ambientais/15842-biomas.html> · Arquivos: <https://geoftp.ibge.gov.br/informacoes_ambientais/estudos_ambientais/biomas/vetores/> | 16/11/2026 | Dados abertos; citar o IBGE |
| Focos de queimadas | INPE — Programa Queimadas / BDQueimadas: <https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/> | 19/11/2026 | Dados públicos; citar o INPE |

Ano/versão da malha municipal do IBGE: [PREENCHER]. Detalhes de tratamento no `DICIONÁRIO.md`. Licença: dados abertos de órgãos públicos, com atribuição às fontes (IBGE e INPE).

## Requisitos

Versões usadas nos testes (Windows):

- PostgreSQL 19.0 (x86_64-windows)
- PostGIS 3.7.0 (GEOS 3.15.0, PROJ 9.8.1)
- GDAL/OGR (`ogr2ogr`) — instalado com o QGIS (OSGeo4W Shell) ou `gdal-bin` no Linux

## Como importar (testado em banco limpo)

Os dados tratados estão em GeoPackage (`dados/tratados/*.gpkg`) e são carregados com `ogr2ogr` (GDAL). No Windows, use o terminal **OSGeo4W Shell** (instalado com o QGIS); no Linux, instale com `sudo apt install gdal-bin`.

```bash
# 1. criar o banco
createdb -U postgres coletas

# 2. criar extensão, tabelas, restrições e índices
psql -U postgres -d coletas -f SQL/esquema.sql

# 3. importar os dados, a partir da raiz do projeto
#    (substitua <SEU_USUARIO> e <SUA_SENHA>; a ordem importa por causa das chaves estrangeiras)
ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 dbname=coletas user=<SEU_USUARIO> password=<SUA_SENHA>" dados/tratados/biomas_tratados.gpkg biomas_tratados -nln public.biomas -lco GEOMETRY_NAME=geom -append -preserve_fid

ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 dbname=coletas user=<SEU_USUARIO> password=<SUA_SENHA>" dados/tratados/municipios_tratados.gpkg municipios_tratados -nln public.municipios -lco GEOMETRY_NAME=geom -append -preserve_fid

ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 dbname=coletas user=<SEU_USUARIO> password=<SUA_SENHA>" dados/tratados/focos_queimadas_tratados.gpkg foco_queimadas -nln public.focos_incendios -lco GEOMETRY_NAME=geom -append -preserve_fid
```

Conferência:

```sql
SELECT 'municipios' AS tabela, count(*) FROM municipios
UNION ALL SELECT 'biomas', count(*) FROM biomas
UNION ALL SELECT 'focos_incendios', count(*) FROM focos_incendios;
```

## Estrutura do repositório

```
├── README.md
├── DICIONÁRIO.md          # dicionário de dados
├── Artefatos/
│   ├── Diagrama_Relacionamento.pdf
│   └── ER-relacional.pdf
├── SQL/
│   ├── esquema.sql        # extensão, tabelas, restrições e índices
│   └── dados.md           # instruções de importação dos dados (ogr2ogr)
├── dados/
│   ├── brutos/            # dados originais, como coletados
│   └── tratados/          # GeoPackages prontos para importação
├── .gitattributes
└── .gitignore
```