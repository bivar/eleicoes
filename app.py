# -*- coding: utf-8 -*-
"""
Data App em Streamlit: Avaliação Socioeconômica do Brasil nos Últimos 6 Mandatos Presidenciais (2003–2026)
Execute localmente com:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import MANDATOS_CICLO, MANDATOS_SEPARADOS, INDICADORES
from src.etl_apis import load_consolidated_data, fetch_bcb_sgs_series
from src.metrics import calcular_resumo_mandatos

st.set_page_config(
    page_title="Painel Socioeconômico do Brasil (2003–2026)",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def get_data() -> pd.DataFrame:
    return load_consolidated_data()

df = get_data()

# Sidebar de Configuração e Filtros
st.sidebar.title("🇧🇷 Painel Socioeconômico")
st.sidebar.caption("Avaliação Comparativa de Mandatos Presidenciais (2003–2026) com Dados Abertos Oficiais")

modo_mandato = st.sidebar.radio(
    "Recorte do Ciclo 2015–2018:",
    options=["Ciclo Eleitoral Unificado (6 Mandatos)", "Governos Separados: Dilma II e Temer (7 Governos)"],
    index=0,
    help="Permite analisar 2015–2018 como um único ciclo constitucional de 4 anos ou separar Dilma II (2015–2016) e Michel Temer (2016–2018)."
)

col_grupo = "mandato_ciclo" if "Unificado" in modo_mandato else "governo_detalhado"
lista_mandatos_cfg = MANDATOS_CICLO if "Unificado" in modo_mandato else MANDATOS_SEPARADOS
mapa_cores = {m["id"]: m["cor"] for m in lista_mandatos_cfg}

eixos_disponiveis = sorted(list({v["eixo"] for v in INDICADORES.values()}))
eixo_selecionado = st.sidebar.selectbox("1. Eixo Temático:", options=eixos_disponiveis, index=eixos_disponiveis.index("Macroeconomia"))

indicadores_do_eixo = {k: v for k, v in INDICADORES.items() if v["eixo"] == eixo_selecionado}
cod_indicador = st.sidebar.selectbox(
    "2. Indicador Socioeconômico:",
    options=list(indicadores_do_eixo.keys()),
    format_func=lambda k: f"{INDICADORES[k]['nome']} ({INDICADORES[k]['unidade']})"
)

meta_ind = INDICADORES[cod_indicador]

mandatos_ativos = st.sidebar.multiselect(
    "3. Filtrar Mandatos:",
    options=[m["id"] for m in lista_mandatos_cfg],
    default=[m["id"] for m in lista_mandatos_cfg]
)

df_filtrado = df[df[col_grupo].isin(mandatos_ativos)].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Fonte Oficial:** [{meta_ind['fonte']}]({meta_ind['url']})")
st.sidebar.caption(f"Código API / Série: `{meta_ind['codigo_api']}`")

# Cabeçalho Principal
st.title("📊 Observatório Socioeconômico dos Mandatos Presidenciais (2003–2026)")
st.markdown(
    f"**Eixo:** `{meta_ind['eixo']}` | **Indicador Selecionado:** **{meta_ind['nome']} ({meta_ind['unidade']})** — "
    f"*{meta_ind['descricao']}* ([Fonte Oficial]({meta_ind['url']}))"
)

# Resumo por mandato
df_resumo = calcular_resumo_mandatos(df_filtrado, cod_indicador, meta_ind["tipo_agregacao"], col_grupo)

# Cards de KPI por mandato
cols_kpi = st.columns(len(df_resumo)) if len(df_resumo) > 0 else []
for idx, row in df_resumo.iterrows():
    with cols_kpi[idx]:
        st.metric(
            label=row["Mandato"],
            value=row["Resumo Principal"],
            delta=row["Detalhe"],
            delta_color="normal" if meta_ind["polaridade"] == "maior_melhor" else (
                "inverse" if meta_ind["polaridade"] == "menor_melhor" else "off"
            )
        )

# Abas de Análise
aba1, aba2, aba3, aba4 = st.tabs([
    "🏆 Scorecard Presidencial",
    "📈 Série Histórica (2003–2026)",
    "⚖️ Comparador Lado a Lado (Ano 1 ao Ano 4)",
    "🔗 APIs Abertas & Base de Dados"
])

with aba1:
    c1, c2 = st.columns([3, 2])
    with c1:
        fig_bar = px.bar(
            df_resumo,
            x="Mandato",
            y="Média Anual",
            color="Mandato",
            color_discrete_map=mapa_cores,
            text="Média Anual",
            title=f"Média Anual por Mandato — {meta_ind['nome']} ({meta_ind['unidade']})"
        )
        fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_bar.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        fig_var = px.bar(
            df_resumo,
            x="Mandato",
            y="Acumulado / Variação no Mandato",
            color="Mandato",
            color_discrete_map=mapa_cores,
            text="Acumulado / Variação no Mandato",
            title=f"Acumulado ou Variação no Período ({meta_ind['unidade']})"
        )
        fig_var.update_traces(texttemplate="%{text:+.2f}", textposition="outside")
        fig_var.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig_var, use_container_width=True)

    st.subheader("Tabela Comparativa Detalhada por Mandato")
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)

with aba2:
    fig_ts = go.Figure()
    for m in lista_mandatos_cfg:
        if m["id"] in mandatos_ativos:
            fig_ts.add_vrect(
                x0=m["inicio"] - 0.5,
                x1=m["fim"] + 0.5,
                fillcolor=m["cor"],
                opacity=0.10,
                line_width=0,
                annotation_text=m["id"].split(" (")[0],
                annotation_position="top left"
            )

    fig_ts.add_trace(go.Scatter(
        x=df_filtrado["ano"],
        y=df_filtrado[cod_indicador],
        mode="lines+markers+text",
        text=[f"{v:.1f}" for v in df_filtrado[cod_indicador]],
        textposition="top center",
        line=dict(color="#0f172a", width=3),
        marker=dict(size=9, color=[mapa_cores.get(g, "#334155") for g in df_filtrado[col_grupo]]),
        name=meta_ind["nome"]
    ))
    fig_ts.update_layout(
        title=f"Evolução Histórica Anual (2003–2026) — {meta_ind['nome']} ({meta_ind['unidade']})",
        xaxis_title="Ano",
        yaxis_title=meta_ind["unidade"],
        height=480,
        xaxis=dict(dtick=1)
    )
    st.plotly_chart(fig_ts, use_container_width=True)

with aba3:
    modo_comp = st.radio(
        "Modo de Normalização da Trajetória:",
        options=["Valor Original no Ano do Mandato (Ano 1 ao Ano 4)", "Índice Base 100 (1º Ano do Mandato = 100)"],
        horizontal=True
    )
    df_traj = df_filtrado.copy()
    if "Base 100" in modo_comp:
        df_traj["valor_plot"] = df_traj.groupby(col_grupo)[cod_indicador].transform(
            lambda s: (s / s.iloc[0]) * 100.0 if s.iloc[0] != 0 else s
        )
        y_label = "Índice (Ano 1 = 100)"
    else:
        df_traj["valor_plot"] = df_traj[cod_indicador]
        y_label = meta_ind["unidade"]

    fig_comp = px.line(
        df_traj,
        x="ano_mandato",
        y="valor_plot",
        color=col_grupo,
        color_discrete_map=mapa_cores,
        markers=True,
        title=f"Trajetória Comparada por Ano de Mandato — {meta_ind['nome']}",
        labels={"ano_mandato": "Ano do Mandato (1º ao 4º Ano)", "valor_plot": y_label, col_grupo: "Mandato"}
    )
    fig_comp.update_layout(xaxis=dict(dtick=1), height=460)
    st.plotly_chart(fig_comp, use_container_width=True)

with aba4:
    st.subheader("Catálogo de Fontes Abertas e Download da Base Consolidada (2003–2026)")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar Base Consolidada Completa (CSV)",
        data=csv_bytes,
        file_name="dados_socioeconomicos_brasil_2003_2026.csv",
        mime="text/csv"
    )
    df_catalogo = pd.DataFrame([
        {
            "Código Interno": k,
            "Eixo Temático": v["eixo"],
            "Indicador": v["nome"],
            "Unidade": v["unidade"],
            "Série / Tabela API": v["codigo_api"],
            "Fonte Oficial": v["fonte"],
            "URL Oficial": v["url"]
        }
        for k, v in INDICADORES.items()
    ])
    st.dataframe(df_catalogo, use_container_width=True, hide_index=True)
