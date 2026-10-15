# -*- coding: utf-8 -*-
"""
Funções de agregação metodológica para comparar mandatos presidenciais:
- Taxa geométrica composta e anualizada para taxas de variação (PIB, IPCA)
- Soma acumulada e média anual para fluxos (Saldo Comercial, Desmatamento)
- Nível inicial, nível final e variação em pontos/unidades para estoques (Dívida/PIB, Desemprego, Gini, IDEB, Saúde, Segurança)
"""

import numpy as np
import pandas as pd


def calcular_resumo_mandatos(df: pd.DataFrame, col_indicador: str, tipo_agregacao: str, col_grupo: str = "mandato_ciclo") -> pd.DataFrame:
    """Calcula métricas comparativas para cada mandato presidencial."""
    resultados = []
    ordem_mandatos = df[col_grupo].drop_duplicates().tolist()

    for mandato in ordem_mandatos:
        sub = df[df[col_grupo] == mandato].sort_values("ano")
        valores = sub[col_indicador].dropna().values
        if len(valores) == 0:
            continue

        ano_ini, ano_fim = int(sub["ano"].min()), int(sub["ano"].max())
        val_ini, val_fim = float(valores[0]), float(valores[-1])
        media_anual = float(np.mean(valores))

        # Valor de referência imediatamente anterior ao início do mandato (quando disponível)
        idx_primeiro = sub.index[0]
        val_base_anterior = float(df.loc[idx_primeiro - 1, col_indicador]) if idx_primeiro > 0 else val_ini

        if tipo_agregacao == "taxa_composta":
            fator = np.prod([1.0 + (v / 100.0) for v in valores])
            acumulado_mandato = (fator - 1.0) * 100.0
            media_geom = (fator ** (1.0 / len(valores)) - 1.0) * 100.0
            label_principal = f"{media_geom:.2f}% a.a."
            label_secundario = f"Acum.: {acumulado_mandato:+.1f}%"
        elif tipo_agregacao == "fluxo_soma":
            soma_total = float(np.sum(valores))
            acumulado_mandato = soma_total
            label_principal = f"Média: {media_anual:,.1f}"
            label_secundario = f"Total: {soma_total:,.1f}"
        else:
            # estoque_fim ou fluxo_media
            variacao_mandato = val_fim - val_base_anterior
            acumulado_mandato = variacao_mandato
            label_principal = f"Fim: {val_fim:,.2f}"
            label_secundario = f"Var.: {variacao_mandato:+.2f} (Média: {media_anual:,.2f})"

        resultados.append({
            "Mandato": mandato,
            "Período": f"{ano_ini}–{ano_fim}",
            "Anos": len(valores),
            "Início (1º Ano)": round(val_ini, 2),
            "Fim (Último Ano)": round(val_fim, 2),
            "Média Anual": round(media_anual, 2),
            "Acumulado / Variação no Mandato": round(float(acumulado_mandato), 2),
            "Mínimo no Período": round(float(np.min(valores)), 2),
            "Máximo no Período": round(float(np.max(valores)), 2),
            "Resumo Principal": label_principal,
            "Detalhe": label_secundario
        })

    return pd.DataFrame(resultados)
