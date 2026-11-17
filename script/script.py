from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import unicodedata


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

COLUNAS_NUMERICAS = ["DiaSemChuva", "Precipitacao", "RiscoFogo", "FRP", "Latitude", "Longitude"]
COLUNAS_TEXTO = ["Satelite", "Pais", "Estado", "Municipio", "Bioma"]
CHAVE_DEDUPLICACAO = ["DataHora", "Satelite", "Latitude", "Longitude"]
COLUNAS_GEOM_ANTIGAS = ["geom", "the_geom", "geometry", "wkt", "ewkt", "srid"]
SRID_PADRAO = 4674



def remover_acentos(texto: str) -> str:
    """Remove acentos e cedilhas mantendo apenas caracteres ASCII."""
    if pd.isna(texto):
        return texto
    normalizado = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in normalizado if not unicodedata.combining(c))

def carregar_dados(caminho_entrada: Path) -> pd.DataFrame:
    if not caminho_entrada.exists():
        raise FileNotFoundError(f"Ficheiro de entrada não encontrado: {caminho_entrada}")

    sufixo = caminho_entrada.suffix.lower()
    if sufixo == ".csv":
        df = pd.read_csv(
            caminho_entrada,
            sep=None,
            engine="python",
            encoding="utf-8",
            na_values=["", "NA", "N/A", "null", "NULL", "None", "-999", "-999.0"],
        )
    elif sufixo in {".xlsx", ".xlsm", ".xls"}:
        df = pd.read_excel(caminho_entrada, sheet_name=0, engine="openpyxl")
    else:
        raise ValueError(f"Formato não suportado: {sufixo}. Utilize .csv, .xlsx ou .xlsm.")

    logger.info("Registos carregados: %d", len(df))
    return df


def limpar_e_filtrar(df: pd.DataFrame, estado_filtro: str = "MINAS GERAIS") -> pd.DataFrame:
    """Padroniza tipos, converte sentinelas -999 para nulo, filtra e remove duplicados."""
    df = df.copy()

    for col in COLUNAS_TEXTO:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
            df[col] = df[col].replace({"": pd.NA, "NULL": pd.NA, "null": pd.NA})
            df[col] = df[col].map(remover_acentos, na_action="ignore")

    if "Estado" in df.columns:
        df["Estado"] = df["Estado"].str.upper()
    if "Municipio" in df.columns:
        df["Municipio"] = df["Municipio"].str.upper()

    df["DataHora"] = pd.to_datetime(df["DataHora"], errors="coerce")
    invalidos_data = df["DataHora"].isna().sum()
    if invalidos_data > 0:
        logger.warning("A remover %d registos com DataHora inválida.", invalidos_data)
        df = df.dropna(subset=["DataHora"])

    for col in COLUNAS_NUMERICAS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    qtd_999 = (df[COLUNAS_NUMERICAS] == -999).sum().sum()
    df[COLUNAS_NUMERICAS] = df[COLUNAS_NUMERICAS].replace([-999, -999.0], np.nan)
    logger.info("Valores sentinela -999 convertidos para NULL: %d", int(qtd_999))

    total_antes_filtro = len(df)
    if estado_filtro and "Estado" in df.columns:
        estado_normalizado = remover_acentos(estado_filtro).strip().upper()
        df = df[df["Estado"] == estado_normalizado]

    df = df.dropna(subset=["Latitude", "Longitude"])
    df = df[
        df["Latitude"].between(-90.0, 90.0)
        & df["Longitude"].between(-180.0, 180.0)
        & ~((df["Latitude"] == 0.0) & (df["Longitude"] == 0.0))
        ]
    logger.info(
        "Registos removidos na filtragem espacial/estado: %d",
        total_antes_filtro - len(df),
        )

    total_antes_dedup = len(df)
    df = df.drop_duplicates()
    df = (
        df.sort_values(by="FRP", ascending=False, na_position="last")
        .drop_duplicates(subset=CHAVE_DEDUPLICACAO, keep="first")
        .sort_values(by="DataHora", ascending=True)
        .reset_index(drop=True)
    )
    logger.info(
        "Duplicados removidos: %d (restantes: %d)",
        total_antes_dedup - len(df),
        len(df),
        )

    return df


def adicionar_geometria_ewkt(df: pd.DataFrame, srid: int = SRID_PADRAO) -> pd.DataFrame:
    """Gera coluna 'geom' no formato EWKT: SRID=4326;POINT(Longitude Latitude)."""
    df = df.drop(columns=[c for c in df.columns if c.lower() in COLUNAS_GEOM_ANTIGAS])
    df["geom"] = (
            f"SRID={srid};POINT("
            + df["Longitude"].map(lambda x: f"{x:.6f}")
            + " "
            + df["Latitude"].map(lambda y: f"{y:.6f}")
            + ")"
    )
    return df


def executar_pipeline(
        caminho_entrada: Path,
        caminho_saida: Path,
        estado_filtro: str = "MINAS GERAIS",
        srid: int = SRID_PADRAO,
) -> None:
    df = carregar_dados(caminho_entrada)
    df_limpo = limpar_e_filtrar(df, estado_filtro=estado_filtro)
    df_final = adicionar_geometria_ewkt(df_limpo, srid=srid)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(caminho_saida, index=False, encoding="utf-8", na_rep="NULL")
    logger.info("Ficheiro tratado guardado com sucesso em: %s", caminho_saida)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filtra, limpa, converte -999 para NULL e gera geometria EWKT."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("../queimadas_por_estado/queimadas_minas_gerais.xlsx"),
        help="Caminho do ficheiro de entrada.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("../output/queimadas_minas_gerais.csv"),
        help="Caminho do CSV tratado de saída.",
    )
    parser.add_argument(
        "--estado",
        type=str,
        default="MINAS GERAIS",
        help="UF para filtragem (use '' para desativar).",
    )
    parser.add_argument(
        "--srid",
        type=int,
        default=SRID_PADRAO,
        help="Código EPSG/SRID da geometria EWKT (padrão: 4674).",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    executar_pipeline(
        caminho_entrada=args.input,
        caminho_saida=args.output,
        estado_filtro=args.estado,
        srid=args.srid,
    )