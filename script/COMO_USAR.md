# Tratamento e Padronização de Dados

Script em Python para limpeza, filtragem e tratamento de valores ausentes (`-999` → `NULL`), remoção de duplicatas e geração de geometria espacial em formato **EWKT** (`SRID=4674`).

---

## Pré-requisitos

Python 3.9+ instalado e dependências necessárias:

```bash
pip install pandas openpyxl numpy
```

## Como Executar

No terminal, a partir da pasta raiz do projeto, execute o comando indicando o arquivo de entrada (`-i`) e o caminho de saída (`-o`):

```bash
python script/script.py -i queimadas_por_estado/queimadas_minas_gerais.xlsx -o output/queimadas_minas_gerais.csv --estado "" --srid 4674   
```


| Parâmetro       | Descrição                                                                   | Padrão                                            |
| ---------------- | ----------------------------------------------------------------------------- | -------------------------------------------------- |
| `-i`, `--input`  | Caminho do arquivo de entrada e saída (`.csv`, `.xlsx`, `.xlsm` ou `.xls`). | `queimadas_por_estado/queimadas_minas_gerais.xlsx` |
| `-o`, `--output` | Caminho onde o arquivo`.csv` tratado será salvo.                             | `output/queimadas_minas_gerais.csv`                |
| `--estado`       | Filtra os registros pela UF especificada (use`""` para não filtrar).         | `MINAS GERAIS`                                     |
| `--srid`         | Código EPSG/SRID aplicado na coluna de geometria EWKT.                       | `4674`                                             |
