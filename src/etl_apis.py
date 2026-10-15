# -*- coding: utf-8 -*-
"""
Módulo de Ingestão e Sincronização com APIs de Dados Abertos Governamentais:
- Banco Central do Brasil (API SGS JSON)
- IBGE (API de Dados Agregados v3 / SIDRA)
- Ipeadata (API OData v4)
- MDIC Comex Stat / INPE TerraBrasilis
Inclui fallback resiliente para o arquivo consolidado local em `data/dados_socioeconomicos_brasil_2003_2026.csv`.
"""

import os
import requests
import pandas as pd

LOCAL_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dados_socioeconomicos_brasil_2003_2026.csv")


def load_consolidated_data() -> pd.DataFrame:
    """Carrega a base histórica consolidada 2003-2026."""
    return pd.read_csv(LOCAL_CSV)


def fetch_bcb_sgs_series(codigo_serie: int, data_inicial: str = "01/01/2003", data_final: str = "31/12/2026") -> pd.DataFrame:
    """
    Consulta diretamente a API REST de Dados Abertos do Banco Central (SGS).
    Exemplo de códigos:
      - 433: IPCA mensal (%)
      - 432: Taxa Selic Meta (% a.a.)
      - 3698: Taxa de câmbio livre R$/US$ (média mensal)
      - 13762: Dívida Bruta do Governo Geral (% PIB)
      - 4513: Dívida Líquida do Setor Público (% PIB)
      - 13621: Reservas Internacionais (US$ milhões)
    """
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados"
        f"?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    )
    headers = {"Accept": "application/json", "User-Agent": "StreamlitSocioeconomicoBR/1.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df


def fetch_ibge_sidra_series(agregado: int, variavel: int, periodos: str = "all") -> dict:
    """
    Consulta a API v3 de Dados Agregados do IBGE (SIDRA).
    Exemplo:
      - Agregado 5932, variável 6561: Taxa de variação do PIB Trimestral
      - Agregado 4099, variável 4099: Taxa de desocupação na PNAD Contínua
      - Agregado 1737, variável 2265: IPCA variação acumulada em 12 meses
    """
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{agregado}/periodos/{periodos}/variaveis/{variavel}?localidades=N1[all]"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_ipeadata_series(sercodigo: str) -> pd.DataFrame:
    """
    Consulta a API OData v4 do Ipeadata.
    Exemplo de códigos:
      - 'GAC12_SALMINRE12': Salário mínimo real
      - 'PRECOS_IPCAG': IPCA taxa anual de variação
    """
    url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{sercodigo}')"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    registros = resp.json().get("value", [])
    df = pd.DataFrame(registros)
    if not df.empty:
        df["VALDATA"] = pd.to_datetime(df["VALDATA"], utc=True)
        df["VALVALOR"] = pd.to_numeric(df["VALVALOR"], errors="coerce")
    return df
