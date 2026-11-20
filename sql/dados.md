# Importação dos dados a partir dos arquivos .gpkg

**1.** Verifique se **ogr2ogr** está instalado:

```bash
ogr2ogr --version

ogrinfo --formats | grep PostgreSQL # verifica se o driver do PostgreSQL está disponível
```

Se não tiver instalado:

```bash
sudo apt update
sudo apt install gdal-bin
```

**2.** Importe os arquivos a partir da **raiz do projeto**:

**OBS**: substitua os dados de acesso ao PostgresSQL pelo seu usuário e senha utilizado.

```bash
ogr2ogr -f PostgreSQL   PG:"host=localhost port=5432 dbname=coletas user=<SEU_USUÁRIO> password=<SUA _SENHA>"   dados/tratados/biomas_tratados.gpkg biomas_tratados   -nln public.biomas   -lco GEOMETRY_NAME=geom

ogr2ogr -f PostgreSQL   PG:"host=localhost port=5432 dbname=coletas user=<SEU_USUÁRIO> password=<SUA _SENHA>"   dados/tratados/municipios_tratados.gpkg municipios_tratados   -nln public.municipios  -lco GEOMETRY_NAME=geom

ogr2ogr -f PostgreSQL   PG:"host=localhost port=5432 dbname=coletas user=<SEU_USUÁRIO> password=<SUA _SENHA>"   dados/tratados/focos_queimadas_tratados.gpkg foco_queimadas   -nln public.focos_incendios -lco GEOMETRY_NAME=geom
```