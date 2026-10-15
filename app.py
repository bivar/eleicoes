# -*- coding: utf-8 -*-
"""
Data App em Streamlit: Observatório Socioeconômico do Brasil nos Últimos 6 Mandatos Presidenciais (2003–2026)
- Página Inicial Explicativa ('🏠 Apresentação do Projeto') para público geral
- Fotos redondas dos governantes e linguagem acessível com insights interpretativos
- Gráficos Plotly sem sobreposição de eixos/legendas (automargin, rótulos em 2 linhas, barra de ferramentas oculta)
- Renderizador HTML/CDN imune ao erro `PlotlyChart.js` no Streamlit Community Cloud
Execute localmente com:
    streamlit run app.py
"""

import importlib
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import src.config as cfg_module
importlib.reload(cfg_module)

from src.config import MANDATOS_CICLO, MANDATOS_SEPARADOS, INDICADORES
from src.etl_apis import load_consolidated_data
from src.metrics import calcular_resumo_mandatos

st.set_page_config(
    page_title="Análise de Mandatos Presidenciais (2003–2026)",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)


def formatar_rotulo_eixo_x(mandato_str: str) -> str:
    """Quebra o nome do mandato em duas linhas curtas para nunca sobrepor no eixo X."""
    if " (" in mandato_str:
        nome, periodo = mandato_str.split(" (", 1)
        periodo = periodo.rstrip(")")
        return f"<b>{nome}</b><br><span style='font-size:11px;color:#64748b'>{periodo}</span>"
    return mandato_str


def mostrar_grafico_plotly(fig, height: int = 450, show_legend: bool = False) -> None:
    """
    Renderiza gráficos Plotly via HTML/CDN sem sobreposição de títulos, eixos ou legendas,
    contornando também o erro `PlotlyChart.<hash>.js` no Streamlit Community Cloud.
    """
    fig.update_layout(
        title=dict(
            x=0.01,
            xanchor="left",
            y=0.96,
            yanchor="top",
            font=dict(size=15, family="Inter, sans-serif", color="#0f172a")
        ),
        margin=dict(l=55, r=25, t=68, b=72 if show_legend else 58),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8fafc",
        font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
        height=height - 18,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            font=dict(size=11)
        ) if show_legend else dict()
    )
    fig.update_xaxes(
        automargin=True,
        tickangle=0,
        title_text=None,
        gridcolor="#eef2f6",
        linecolor="#cbd5e1"
    )
    fig.update_yaxes(
        automargin=True,
        title_standoff=12,
        gridcolor="#e2e8f0",
        zerolinecolor="#94a3b8",
        zerolinewidth=1.5
    )

    html_str = fig.to_html(
        include_plotlyjs="cdn",
        full_html=False,
        config={"displayModeBar": False, "responsive": True, "displaylogo": False}
    )
    wrapper = f"""
    <div style="width:100%; overflow:hidden; background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:8px; box-sizing:border-box;">
        {html_str}
    </div>
    """
    components.html(wrapper, height=height, scrolling=False)


# Fallbacks defensivos caso o ambiente tenha uma versão anterior de src/config.py
DEFAULT_FOTOS = {
    "Lula I (2003–2006)": ("https://upload.wikimedia.org/wikipedia/commons/3/3b/Lula_-_foto_oficial_-_05_jan_2007_%283x4_cropped%29.jpg", None),
    "Lula II (2007–2010)": ("https://upload.wikimedia.org/wikipedia/commons/3/3b/Lula_-_foto_oficial_-_05_jan_2007_%283x4_cropped%29.jpg", None),
    "Dilma I (2011–2014)": ("https://upload.wikimedia.org/wikipedia/commons/8/81/Dilma_Rousseff_-_foto_oficial_2011-01-09.jpg", None),
    "Dilma II / Temer (2015–2018)": (
        "https://upload.wikimedia.org/wikipedia/commons/8/81/Dilma_Rousseff_-_foto_oficial_2011-01-09.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9b/Presidente_Michel_Temer_%28foto_oficial%29_-_cortada.jpg"
    ),
    "Dilma II (2015–2016)": ("https://upload.wikimedia.org/wikipedia/commons/8/81/Dilma_Rousseff_-_foto_oficial_2011-01-09.jpg", None),
    "Temer (2016–2018)": ("https://upload.wikimedia.org/wikipedia/commons/9/9b/Presidente_Michel_Temer_%28foto_oficial%29_-_cortada.jpg", None),
    "Bolsonaro (2019–2022)": ("https://upload.wikimedia.org/wikipedia/commons/a/a6/Jair_Bolsonaro%2C_Presidente_da_Rep%C3%BAblica_Federativa_do_Brasil_%28cropped%29.jpg", None),
    "Lula III (2023–2026)": ("https://upload.wikimedia.org/wikipedia/commons/8/84/Foto_oficial_de_Luiz_In%C3%A1cio_Lula_da_Silva_%28quadrada%29.jpg", None),
}

DEFAULT_ICONES = {
    "pib_cresc_aa": "📈",
    "ipca_aa": "🛒",
    "selic_meta_fim": "🏦",
    "cambio_medio": "💵",
    "divida_bruta_pib": "🏛️",
    "divida_liquida_pib": "⚖️",
    "resultado_primario_pib": "🧾",
    "desemprego_medio": "💼",
    "salario_minimo_real_2026": "🪙",
    "gini_renda": "🤝",
    "taxa_pobreza_pct": "🏘️",
    "ideb_anos_iniciais": "📚",
    "ideb_ensino_medio": "🎓",
    "taxa_analfabetismo_15m": "✏️",
    "mortalidade_infantil_mil": "👶",
    "expectativa_vida_anos": "❤️",
    "taxa_homicidios_100m": "🛡️",
    "desmatamento_amazonia_km2": "🌳",
    "saldo_comercial_us_bi": "🚢",
    "reservas_internacionais_us_bi": "🛡️",
}

DEFAULT_EXPLICACOES = {
    "pib_cresc_aa": (
        "Pense no PIB como o 'tamanho do bolo' da economia brasileira. Quando o PIB cresce, há mais empresas vendendo, mais obras e maior geração de renda; quando fica negativo, o país está em recessão.",
        "O Brasil viveu seu ciclo de maior expansão em Lula II (+4,58% a.a. na média composta), sofreu forte recessão em 2015–2016 (-3,55% e -3,28%), enfrentou o choque da pandemia em 2020 (-3,28%) seguido de recuperação e manteve expansão média próxima de 2,7% a.a. entre 2023 e 2026."
    ),
    "ipca_aa": (
        "Mede o quanto o custo de vida subiu no supermercado, transporte, saúde e moradia. Quanto menor e mais controlada a inflação, mais o seu salário rende até o fim do mês.",
        "Os dois maiores picos inflacionários desde 2003 ocorreram em 2015 (10,67%, com o realinhamento de tarifas) e em 2021 (10,06%, sob choque global na pandemia). As menores taxas anuais foram registradas em 2017 (2,95%) e 2006 (3,14%)."
    ),
    "selic_meta_fim": (
        "A Selic é o 'freio' que o Banco Central usa para controlar a inflação. Quando ela sobe, financiamentos, cartões e empréstimos ficam mais caros; quando cai, o crédito fica mais barato.",
        "Caiu dos patamares de 16%–18% em 2003–2005 para 6,5% em 2018 e 2,0% em 2020 na pandemia, voltando a operar acima de 11%–14% entre 2022 e 2026 para conter a inflação."
    ),
    "cambio_medio": (
        "Mostra quantos reais são necessários para comprar 1 dólar. Dólar mais alto encarece eletrônicos, trigo e combustíveis, mas aumenta a receita em reais de quem exporta.",
        "O Real valorizou-se entre 2003 (R$ 3,07) e 2011 (R$ 1,67), subiu para a faixa de R$ 3,30–R$ 3,90 a partir de 2015 e mudou para o patamar acima de R$ 5,00 a partir da pandemia em 2020."
    ),
    "divida_bruta_pib": (
        "Funciona como comparar o saldo devedor de uma família com a sua renda anual. Se a dívida cresce muito mais rápido que o PIB, o governo gasta cada vez mais impostos pagando juros.",
        "Manteve-se entre 48% e 56% do PIB de 2003 a 2014, subiu quase 20 p.p. entre 2014 e 2018 (75,3%), atingiu 86,9% em 2020 na pandemia, recuou a 71,7% em 2022 e subiu para 81,9% até 2026."
    ),
    "divida_liquida_pib": (
        "É a dívida do governo descontando o 'dinheiro guardado no cofre' (como as reservas em dólar do Banco Central).",
        "Caiu de 54,3% do PIB em 2003 para a mínima de 30,5% em 2013 com superávits e acúmulo de reservas, voltando a subir desde 2014 até 65,1% do PIB em 2026."
    ),
    "resultado_primario_pib": (
        "Mostra se o governo fechou o ano no azul (superávit, economizando para abater juros) ou no vermelho (déficit, gastando mais do que arrecadou em impostos).",
        "De 2003 a 2013 houve superávits contínuos entre 1,7% e 3,7% do PIB. Em 2014 iniciou-se um ciclo de déficits (com pico de -9,24% em 2020 na pandemia), voltando ao azul em 2021–2022 e operando próximo da estabilidade entre 2024 e 2026."
    ),
    "desemprego_medio": (
        "De cada 100 brasileiros que querem trabalhar e estão procurando vaga, quantos estão sem trabalho no momento.",
        "Recuou de 12,3% em 2003 para ~6,0%–6,9% em 2011–2014, subiu na recessão de 2015–2017 e atingiu 13,8% na pandemia (2020), caindo fortemente até a mínima histórica de 5,4% em 2026."
    ),
    "salario_minimo_real_2026": (
        "Mostra quanto o salário mínimo daquela época compraria hoje, já descontando toda a inflação.",
        "Quase dobrou em termos reais em 23 anos: saiu de R$ 998 em 2003 para R$ 1.694 em 2014, ficou estável entre 2015 e 2022 e retomou ganhos reais até R$ 1.936 em 2026."
    ),
    "gini_renda": (
        "Mede a distância entre os mais ricos e os mais pobres. Quanto menor esse número, melhor distribuída está a renda entre as famílias brasileiras.",
        "Caiu de 0,581 em 2003 para 0,515 em 2015, piorou entre 2016 e 2018 com a crise do emprego e atingiu a mínima histórica em 2024 (0,504)."
    ),
    "taxa_pobreza_pct": (
        "De cada 100 moradores do país, quantos têm renda familiar insuficiente para cobrir necessidades básicas.",
        "Caiu de 41,8% (2003) para 22,8% (2014), subiu na crise de 2015–2017 e em 2021 (36,7%), recuando para a mínima histórica de 22,4%–23,1% em 2024–2026."
    ),
    "ideb_anos_iniciais": (
        "É o boletim das escolas brasileiras para crianças de 6 a 10 anos (1º ao 5º ano), indo de 0 a 10.",
        "Subiu de forma consistente em quase todos os governos desde 2003 (de 3,6 para 6,2 em 2026)."
    ),
    "ideb_ensino_medio": (
        "Avalia o aprendizado dos jovens no Ensino Médio e a aprovação escolar, historicamente o maior gargalo da educação básica.",
        "Ficou estagnado em 3,7 entre 2010 e 2015, subiu para 4,2 em 2019 e alcançou 4,4–4,5 entre 2024 e 2026."
    ),
    "taxa_analfabetismo_15m": (
        "Mostra a parcela da população de 15 anos ou mais que ainda não sabe ler e escrever um bilhete simples.",
        "Caiu a menos da metade ao longo dos 6 mandatos: de 11,6% em 2003 para 5,1% em 2026."
    ),
    "mortalidade_infantil_mil": (
        "Quantos bebês falecem antes de completar 1 ano para cada 1.000 nascidos vivos. Termômetro direto de saúde pública, vacinação e saneamento.",
        "Caiu mais de 60% em duas décadas, saindo de 24,68 por mil em 2003 para 9,88 por mil em 2026."
    ),
    "expectativa_vida_anos": (
        "Mostra quantos anos, em média, um recém-nascido brasileiro espera viver.",
        "Subiu de 71,3 anos (2003) para 76,4 anos (2019), recuou temporariamente a 72,8 anos em 2021 devido à pandemia de COVID-19 e atingiu 77,0 anos em 2026."
    ),
    "taxa_homicidios_100m": (
        "Quantos assassinatos são registrados no país para cada 100 mil habitantes.",
        "Subiu até o pico histórico de 31,6 por 100 mil em 2017 e entrou em queda consistente a partir de 2018 até atingir ~19,8–20,6 por 100 mil em 2024–2026."
    ),
    "desmatamento_amazonia_km2": (
        "Equivale à área de floresta nativa derrubada por ano na Amazônia Legal medida por satélite pelo INPE.",
        "Caiu de 27.772 km² (2004) para a mínima histórica de 4.571 km² (2012), voltou a subir entre 2019 e 2022 (pico de 13.038 km² em 2021) e recuou mais de 50% entre 2023 e 2025/2026."
    ),
    "saldo_comercial_us_bi": (
        "Mostra se o Brasil vendeu mais produtos para o exterior do que comprou de outros países (em US$ bilhões).",
        "Ganhou forte tração na última década com o agronegócio e o petróleo do pré-sal, batendo recordes históricos entre 2023 (US$ 98,9 bi) e 2025 (US$ 68,3 bi)."
    ),
    "reservas_internacionais_us_bi": (
        "É a 'poupança em dólar' do Brasil mantida pelo Banco Central para proteger o país contra crises externas.",
        "Multiplicou-se por 7 vezes entre 2003 (US$ 49,3 bi) e 2012 (US$ 373,1 bi), mantendo-se desde então entre US$ 325 bi e US$ 375 bi."
    ),
}


def get_icone(k: str) -> str:
    return INDICADORES.get(k, {}).get("icone", DEFAULT_ICONES.get(k, "📊"))


def get_explicacao_leigo(k: str) -> str:
    info = INDICADORES.get(k, {})
    if "explicacao_leigo" in info:
        return info["explicacao_leigo"]
    return DEFAULT_EXPLICACOES.get(k, (info.get("descricao", ""), ""))[0]


def get_insight_geral(k: str) -> str:
    info = INDICADORES.get(k, {})
    if "insight_geral" in info:
        return info["insight_geral"]
    return DEFAULT_EXPLICACOES.get(k, ("", "Série histórica oficial consolidada entre 2003 e 2026."))[1]


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_consolidated_data()


df = get_data()

# Sidebar amigável com keys explícitas
st.sidebar.title("🇧🇷 Comparação entre Mandatos 🇧🇷 ")
st.sidebar.caption("Comparativo Visual de Mandatos Presidenciais (2003–2026) com Dados Abertos Oficiais")

modo_mandato = st.sidebar.radio(
    "Como exibir 2015–2018?",
    options=["Ciclo Eleitoral Unificado (6 Mandatos)", "Governos Separados: Dilma II e Temer (7 Governos)"],
    index=0,
    key="radio_modo_mandato"
)

col_grupo = "mandato_ciclo" if "Unificado" in modo_mandato else "governo_detalhado"
lista_mandatos_cfg = MANDATOS_CICLO if "Unificado" in modo_mandato else MANDATOS_SEPARADOS
mapa_cores = {m["id"]: m["cor"] for m in lista_mandatos_cfg}
mapa_cfg = {m["id"]: m for m in lista_mandatos_cfg}

eixos_disponiveis = sorted(list({v["eixo"] for v in INDICADORES.values()}))
eixo_selecionado = st.sidebar.selectbox(
    "1. Escolha o Tema:",
    options=eixos_disponiveis,
    index=eixos_disponiveis.index("Macroeconomia"),
    key="sb_eixo_tematico"
)

indicadores_do_eixo = {k: v for k, v in INDICADORES.items() if v["eixo"] == eixo_selecionado}
cod_indicador = st.sidebar.selectbox(
    "2. Escolha o Indicador:",
    options=list(indicadores_do_eixo.keys()),
    format_func=lambda k: f"{get_icone(k)} {INDICADORES[k]['nome']} ({INDICADORES[k]['unidade']})",
    key="sb_indicador_socioeconomico"
)

meta_ind = INDICADORES[cod_indicador]
icone_ind = get_icone(cod_indicador)
explicacao_leigo = get_explicacao_leigo(cod_indicador)
insight_geral = get_insight_geral(cod_indicador)

mandatos_ativos = st.sidebar.multiselect(
    "3. Governos Comparados:",
    options=[m["id"] for m in lista_mandatos_cfg],
    default=[m["id"] for m in lista_mandatos_cfg],
    key="ms_governos_comparados"
)

df_filtrado = df[df[col_grupo].isin(mandatos_ativos)].copy()

# Abas Principais (incluindo Apresentação e a nova página de Conclusão & Balanço Geral)
aba_home, aba_conclusao, aba1, aba2, aba3, aba4 = st.tabs([
    "🏠 Apresentação do Projeto",
    "🎯 Conclusão & Balanço Geral",
    "🏆 Comparativo por Governo",
    "📈 Linha do Tempo (2003–2026)",
    "⚖️ Evolução do 1º ao 4º Ano",
    "🔗 Fontes & Download CSV"
])

with aba_home:
    st.markdown(
        """
        <div style="background:linear-gradient(135deg, #0f172a 0%, #064e3b 100%); color:#ffffff; border-radius:18px; padding:28px 32px; margin-bottom:20px;">
            <span style="background:rgba(16,185,129,0.2); border:1px solid rgba(52,211,153,0.4); color:#6ee7b7; font-size:12px; font-weight:700; padding:4px 12px; border-radius:999px; text-transform:uppercase; letter-spacing:0.05em;">
                Dados Abertos Oficiais • Para todos • 2003 a 2026
            </span>
            <h1 style="color:#ffffff; font-size:28px; font-weight:800; margin:12px 0 8px 0;">
                🇧🇷 Análise de Mandatos Presidenciais 🇧🇷
            </h1>
            <p style="color:#cbd5e1; font-size:15px; line-height:1.6; max-width:920px; margin:0;">
                Este projeto nasceu para aproximar os cidadões dos indicadores oficiais do Brasil e nos preparar para o segundo turno da eleição de 2026.
                Trouxe <b>6 ciclos presidenciais (2003–2026)</b>. Todas as <b>20 séries históricas</b> são públicas e estão dispostas
                em gráficos claros, explicações do dia a dia e contexto histórico para que qualquer um possa comparar governos com base em fatos verificáveis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Governos e Períodos Analisados (2003–2026)")
    cols_pres = st.columns(len(lista_mandatos_cfg))
    resumos_curtos_home = {
        "Lula I (2003–2006)": "Ajuste externo, boom de commodities, queda da inflação e criação do Bolsa Família.",
        "Lula II (2007–2010)": "Forte expansão do PIB e do emprego formal, valorização do salário mínimo e enfrentamento da crise global de 2008/2009.",
        "Dilma I (2011–2014)": "Baixo desemprego e mínima histórica de desmatamento em 2012, mas desaceleração do PIB e deterioração fiscal em 2014.",
        "Dilma II / Temer (2015–2018)": "Forte recessão e inflação em 2015–2016, impeachment em 2016, aprovação do Teto de Gastos e queda da inflação/Selic em 2017–2018.",
        "Dilma II (2015–2016)": "Baque recessivo, realinhamento de tarifas represadas e crise política que culminou no impeachment em 2016.",
        "Temer (2016–2018)": "Controle da inflação (2,95% em 2017), queda da Selic a 6,5%, Teto de Gastos e reforma trabalhista.",
        "Bolsonaro (2019–2022)": "Choque global da pandemia de COVID-19 (2020–2021), queda nos homicídios (devido ao COVID) e retomada do PIB/emprego em 2021–2022 com uma alta de juros.",
        "Lula III (2023–2026)": "Recordes na balança comercial, mínimas históricas de desemprego e Gini, queda no desmatamento e pressão da dívida sob juros altos."
    }
    for i, m in enumerate(lista_mandatos_cfg):
        m_id = m["id"]
        cor = m["cor"]
        curto = m.get("curto", m_id.split(" (")[0])
        f1, f2 = DEFAULT_FOTOS.get(m_id, ("", None))
        foto1 = m.get("foto") or f1
        foto2 = m.get("foto_extra") or f2
        if foto2:
            avatar_home = (
                f'<div style="display:flex; justify-content:center; margin-bottom:8px;">'
                f'<img src="{foto1}" style="width:52px; height:52px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor}; margin-right:-10px; z-index:2;" />'
                f'<img src="{foto2}" style="width:52px; height:52px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor}; z-index:1;" />'
                f'</div>'
            )
        else:
            avatar_home = (
                f'<img src="{foto1}" style="width:56px; height:56px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor}; margin:0 auto 8px auto; display:block;" />'
            )
        with cols_pres[i]:
            st.markdown(
                f"""
                <div style="border:1px solid #e2e8f0; border-top:4px solid {cor}; border-radius:14px; padding:12px; background:#ffffff; text-align:center; height:100%;">
                    {avatar_home}
                    <div style="font-weight:800; font-size:13px; color:#0f172a;">{curto}</div>
                    <div style="font-size:11px; color:#64748b; margin-bottom:6px;">{m['inicio']}–{m['fim']}</div>
                    <p style="font-size:11px; color:#475569; line-height:1.45; margin:0;">{resumos_curtos_home.get(m_id, '')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("")
    c_guia1, c_guia2 = st.columns(2)
    with c_guia1:
        st.markdown(
            """
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; padding:18px;">
                <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin-top:0;">O que você pode explorar nas abas ao lado?</h3>
                <ul style="font-size:13px; color:#334155; line-height:1.7; padding-left:18px; margin-bottom:0;">
                    <li><b>Macroeconomia & Bolso:</b> Crescimento do PIB Real, Inflação (IPCA), Taxa de Juros Selic e Dólar.</li>
                    <li><b>Contas Públicas:</b> Dívida Bruta (DBGG), Dívida Líquida e Resultado Primário (% do PIB).</li>
                    <li><b>Trabalho & Renda:</b> Taxa de Desemprego e Poder de Compra Real do Salário Mínimo (a preços de 2026).</li>
                    <li><b>Social, Educação & Saúde:</b> Desigualdade (Gini), Pobreza, notas do IDEB, Mortalidade Infantil e Expectativa de Vida.</li>
                    <li><b>Segurança, Amazônia & Setor Externo:</b> Taxa de Homicídios, Desmatamento PRODES/INPE e Saldo da Balança Comercial.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c_guia2:
        st.markdown(
            """
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:14px; padding:18px;">
                <h3 style="font-size:16px; font-weight:800; color:#065f46; margin-top:0;">3 Dicas para Ler os Dados como um Especialista</h3>
                <ol style="font-size:13px; color:#064e3b; line-height:1.7; padding-left:18px; margin-bottom:0;">
                    <li><b>Diferencie Fluxo e Estoque:</b> Indicadores como PIB, Inflação e Balança Comercial somam-se ano a ano (fluxo); já Desemprego, Dívida/PIB e Gini mostram como o país estava no início e no fim de cada mandato (estoque).</li>
                    <li><b>Desconte a Inflação:</b> Comparar salários em valores nominais engana; por isso nosso indicador de Salário Mínimo já está corrigido pelo IPCA para reais de 2026.</li>
                    <li><b>Considere Choques Globais:</b> Crises mundiais (como 2008/2009 e a pandemia de COVID-19 em 2020–2021) ou booms de commodities afetam todos os países ao mesmo tempo.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")

    st.info("**Como começar:** Use o menu lateral à esquerda para escolher o **Tema** e o **Indicador**, e clique na aba **Comparativo por Governo** ou **Linha do Tempo (2003–2026)** logo acima!")

with aba_conclusao:
    st.markdown(
        """
        <div style="background:linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color:#ffffff; border-radius:18px; padding:24px 28px; margin-bottom:18px;">
            <span style="background:rgba(250,204,21,0.2); border:1px solid rgba(250,204,21,0.45); color:#fde047; font-size:11px; font-weight:800; padding:4px 10px; border-radius:999px; text-transform:uppercase;">
                Síntese Executiva • 2003 a 2026
            </span>
            <h2 style="color:#ffffff; font-size:24px; font-weight:800; margin:10px 0 6px 0;">
                Afinal, o que os números dizem sobre os governos?
            </h2>
            <p style="color:#cbd5e1; font-size:14px; line-height:1.55; margin:0;">
                Nenhum mandato venceu em todos os 20 indicadores, mas quando cruzamos <b>Economia no Bolso</b>,
                <b>Contas Públicas</b> e <b>Avanço Social/Ambiental</b>, os dados mostram claramente quem entregou o melhor equilíbrio geral
                e quais foram os acertos e tropeços de cada período.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("1. Quem se destacou em quê? (Destaques por Área)")
    podio_cards = [
        
        {
            "titulo": "💰 Maior Economia Fiscal & Queda Rápida da Pobreza",
            "gov": "Lula I (2003–2006)",
            "cor": "#dc2626",
            "foto": DEFAULT_FOTOS["Lula I (2003–2006)"][0],
            "resumo": "Entregou o maior superávit primário médio (+3,46% do PIB ao ano), derrubou a inflação de 9,3% para 3,1% ao ano e tirou 10% da população da linha de pobreza em 4 anos."
        },
        {
            "titulo": "🏆 Melhor Equilíbrio Geral (Economia + Fiscal + Social)",
            "gov": "Lula II (2007–2010)",
            "cor": "#b91c1c",
            "foto": DEFAULT_FOTOS["Lula II (2007–2010)"][0],
            "resumo": "Maior crescimento do PIB da série (+4,64% ao ano), reduziu a Dívida Bruta (para 51,8% do PIB) com superávit fiscal, triplicou as reservas em dólar, derrubou o desemprego para 6,7% e cortou o desmatamento pela metade."
        },
        {
            "titulo": "🌳 Menor Desmatamento da História & Menor Dívida Líquida",
            "gov": "Dilma I (2011–2014)",
            "cor": "#ea580c",
            "foto": DEFAULT_FOTOS["Dilma I (2011–2014)"][0],
            "resumo": "Atingiu o menor desmatamento já registrado na Amazônia (média de 5.473 km²/ano e mínima de 4.571 km² em 2012) e a menor Dívida Líquida (30,5% do PIB), antes de perder fôlego fiscal em 2014."
        },
        {
            "titulo": "🛒 Controle Rápido da Inflação & Queda dos Juros Pós-Crise",
            "gov": "Temer (2016–2018)",
            "cor": "#0284c7",
            "foto": DEFAULT_FOTOS["Temer (2016–2018)"][0],
            "resumo": "Após a grave recessão de 2015–2016, entregou a menor inflação anual de toda a série (2,95% em 2017), derrubou a Selic de 14,25% para 6,50% e retomou o crescimento do PIB."
        },
        {
            "titulo": "💲 Redução da Dívida/PIB Pós-Pandemia",
            "gov": "Bolsonaro (2019–2022)",
            "cor": "#2563eb",
            "foto": DEFAULT_FOTOS["Bolsonaro (2019–2022)"][0],
            "resumo": "Reduziu a taxa de homicídios de 27,8 para 21,7 por 100 mil hab., avançou no IDEB do Ensino Médio (4,3) e terminou o mandato com Dívida Bruta menor do que recebeu (71,7% vs. 75,3% do PIB)."
        },
        {
            "titulo": "💼 Recorde de Emprego, Salário Real & Balança Comercial",
            "gov": "Lula III (2023–2026)",
            "cor": "#059669",
            "foto": DEFAULT_FOTOS["Lula III (2023–2026)"][0],
            "resumo": "Atingiu o menor desemprego da série (5,4%), o maior salário mínimo real (R$ 1.936), a menor desigualdade (Gini 0,504) e o maior saldo comercial da história (+US$ 305,9 bi), mas com alta na dívida pública."
        }
    ]

    cols_podio_1 = st.columns(3)
    for idx in range(3):
        c = podio_cards[idx]
        cor_c, titulo_c, foto_c, gov_c, resumo_c = c["cor"], c["titulo"], c["foto"], c["gov"], c["resumo"]
        eh_vencedor_geral = (gov_c == "Lula II (2007–2010)")
        bg_card = "linear-gradient(180deg, #dcfce7 0%, #ecfdf5 100%)" if eh_vencedor_geral else "#ffffff"
        border_card = "2px solid #22c55e" if eh_vencedor_geral else "1px solid #e2e8f0"
        selo_vencedor = (
            '<div style="margin-bottom:6px;"><span style="display:inline-block; background:#16a34a; color:#ffffff; font-size:10px; font-weight:800; padding:2px 8px; border-radius:999px; text-transform:uppercase;">★ Vencedor Geral nos Dados</span></div>'
            if eh_vencedor_geral else ""
        )
        card_html = (
            f'<div style="border:{border_card}; border-left:5px solid {cor_c}; border-radius:14px; padding:14px; background:{bg_card}; margin-bottom:12px; min-height:175px;">'
            f'{selo_vencedor}'
            f'<div style="font-size:11px; font-weight:800; color:{cor_c}; text-transform:uppercase; margin-bottom:8px;">{titulo_c}</div>'
            f'<div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">'
            f'<img src="{foto_c}" style="width:44px; height:44px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor_c};" />'
            f'<div style="font-weight:800; font-size:15px; color:#0f172a;">{gov_c}</div>'
            f'</div>'
            f'<p style="font-size:12px; color:#475569; line-height:1.5; margin:0;">{resumo_c}</p>'
            f'</div>'
        )
        with cols_podio_1[idx]:
            st.markdown(card_html, unsafe_allow_html=True)

    cols_podio_2 = st.columns(3)
    for idx in range(3, 6):
        c = podio_cards[idx]
        cor_c, titulo_c, foto_c, gov_c, resumo_c = c["cor"], c["titulo"], c["foto"], c["gov"], c["resumo"]
        card_html = (
            f'<div style="border:1px solid #e2e8f0; border-left:5px solid {cor_c}; border-radius:14px; padding:14px; background:#ffffff; margin-bottom:12px; min-height:175px;">'
            f'<div style="font-size:11px; font-weight:800; color:{cor_c}; text-transform:uppercase; margin-bottom:8px;">{titulo_c}</div>'
            f'<div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">'
            f'<img src="{foto_c}" style="width:44px; height:44px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor_c};" />'
            f'<div style="font-weight:800; font-size:15px; color:#0f172a;">{gov_c}</div>'
            f'</div>'
            f'<p style="font-size:12px; color:#475569; line-height:1.5; margin:0;">{resumo_c}</p>'
            f'</div>'
        )
        with cols_podio_2[idx - 3]:
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("")
    st.subheader("2. O Último Mandato — Lula III (2023–2026) — foi bom?")
    st.caption("Os dados mostram um governo com **dois lados muito distintos**: **excelente** desempenho no emprego, bolso do trabalhador e meio ambiente, mas pressionado no endividamento público e nos juros.")

    col_pro, col_con = st.columns(2)
    with col_pro:
        st.markdown(
            """
            <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:16px; padding:18px; height:100%;">
                <div style="font-size:15px; font-weight:800; color:#166534; margin-bottom:10px;">
                    🟢 Onde foi MUITO BEM (Economia Real, Social e Ambiental)
                </div>
                <ul style="font-size:13px; color:#14532d; line-height:1.65; padding-left:18px; margin:0;">
                    <li><b>Menor Desemprego da Série (5,4%):</b> Caiu de 9,3% (2022) para a mínima histórica no IBGE, com forte geração de vagas formais.</li>
                    <li><b>Maior Poder de Compra do Salário Mínimo (R$ 1.936):</b> Ganho real de +11,1% descontada toda a inflação do período.</li>
                    <li><b>Mínima Histórica de Desigualdade e Queda da Pobreza:</b> O Índice de Gini atingiu o melhor nível da história em 2024 (0,504) e a pobreza caiu de 31,6% para 22,4%.</li>
                    <li><b>PIB Acima do Esperado (+2,70% a.a.) e Menor Inflação Média (4,41%):</b> Crescimento sustentado pela agropecuária, serviços e consumo, com recorde de US$ 305,9 bi na balança comercial.</li>
                    <li><b>Queda de mais de 50% no Desmatamento:</b> A taxa na Amazônia Legal recuou de 11.594 km² (2022) para 6.518 km² (2024) e 5.731 km² (2025).</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_con:
        st.markdown(
            """
            <div style="background:#fef2f2; border:1px solid #fca5a5; border-radius:16px; padding:18px; height:100%;">
                <div style="font-size:15px; font-weight:800; color:#991b1b; margin-bottom:10px;">
                    🔴 Onde deixou ALGUNS ALERTAS (Dívida e Juros)
                </div>
                <ul style="font-size:13px; color:#7f1d1d; line-height:1.65; padding-left:18px; margin:0;">
                    <li><b>Salto de +10,2 pontos na Dívida Bruta (de 71,7% para 81,9% do PIB):</b> Segundo maior avanço de endividamento da série (atrás apenas da recessão de 2015–2018).</li>
                    <li><b>Quatro Anos Seguidos de Déficit Primário (-0,80% do PIB/ano):</b> Diferente de Lula I e Lula II (que economizavam mais de 2,7% do PIB ao ano), as despesas cresceram acima do necessário para estabilizar a dívida.</li>
                    <li><b>Juros Básicos Muito Altos (Selic entre 11,75% e 14,25%):</b> A dificuldade fiscal manteve as expectativas de inflação pressionadas, levando o Banco Central a manter o crédito caro.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")
    st.subheader("3. Semáforo Resumido dos 6 Ciclos Presidenciais")
    st.caption("Leitura rápida com cores: 🟢 Ponto Forte / Melhora • 🟡 Intermediário / Estável • 🔴 Ponto Crítico / Piora • ⚪ Neutro")

    df_semaforo = pd.DataFrame([
        {
            "Mandato": "Lula I (2003–2006)",
            "Crescimento do PIB": "🟢 +3,51% a.a.",
            "Inflação (IPCA)": "🟡 6,43% a.a. (em queda)",
            "Contas e Dívida (% PIB)": "🟢 Superávit +3,46% | Dívida estável (55,5%)",
            "Emprego e Renda Real": "🟢 Desemprego 10,0% | Salário +25%",
            "Social (Pobreza e Gini)": "🟢 Pobreza caiu 10 p.p. (31,8%)",
            "Amazônia (Desmatamento)": "🟡 Pico em 2004, mas caiu 49% até 2006",
            "Segurança (Homicídios)": "🟢 Caiu de 28,9 para 26,6 /100 mil"
        },
        {
            "Mandato": "Lula II (2007–2010)",
            "Crescimento do PIB": "🟢 +4,64% a.a. (1º lugar)",
            "Inflação (IPCA)": "🟢 5,15% a.a. (na meta)",
            "Contas e Dívida (% PIB)": "🟢 Superávit +2,78% | Dívida caiu a 51,8%",
            "Emprego e Renda Real": "🟢 Desemprego caiu a 6,7% | Salário +21%",
            "Social (Pobreza e Gini)": "🟢 Pobreza caiu a 23,2% | Gini 0,533",
            "Amazônia (Desmatamento)": "🟢 Caiu pela metade (7.000 km² em 2010)",
            "Segurança (Homicídios)": "🟡 Subiu de 26,6 para 27,8 /100 mil"
        },
        {
            "Mandato": "Dilma I (2011–2014)",
            "Crescimento do PIB": "🟡 +2,35% a.a. (0,5% em 2014)",
            "Inflação (IPCA)": "🟡 6,17% a.a. (teto da meta)",
            "Contas e Dívida (% PIB)": "🟡 1º déficit em 2014 (-0,56%) | Dívida 56,3%",
            "Emprego e Renda Real": "🟢 Pleno emprego (6,9%) | Salário R$ 1.694",
            "Social (Pobreza e Gini)": "🟢 Pobreza 22,8% | Gini caiu a 0,518",
            "Amazônia (Desmatamento)": "🟢 Menor da história (média 5.473 km²)",
            "Segurança (Homicídios)": "🔴 Subiu para 29,8 /100 mil"
        },
        {
            "Mandato": "Dilma II / Temer (2015–2018)",
            "Crescimento do PIB": "🔴 -0,93% a.a. (recessão 15–16)",
            "Inflação (IPCA)": "🟡 10,7% (2015) → 🟢 2,95% (2017)",
            "Contas e Dívida (% PIB)": "🔴 Déficit -1,90% | Dívida subiu +19 p.p. (75,3%)",
            "Emprego e Renda Real": "🔴 Desemprego dobrou (12,4%) | Salário estável",
            "Social (Pobreza e Gini)": "🔴 Pobreza subiu a 29,2% | Gini 0,545",
            "Amazônia (Desmatamento)": "🟡 Subiu gradualmente (média 7.146 km²)",
            "Segurança (Homicídios)": "🔴 Recorde em 2017 (31,6), caindo em 2018 (27,8)"
        },
        {
            "Mandato": "Bolsonaro (2019–2022)",
            "Crescimento do PIB": "🟡 +1,43% a.a. (pandemia em 2020)",
            "Inflação (IPCA)": "🔴 6,17% a.a. (pico de 10,1% em 2021)",
            "Contas e Dívida (% PIB)": "🟢 Dívida caiu de 75,3% para 71,7% no fim",
            "Emprego e Renda Real": "🟡 Pico de 13,8% (2020), caindo a 9,3% (2022)",
            "Social (Pobreza e Gini)": "🟡 Pico de pobreza em 2021, Gini 0,518 em 2022",
            "Amazônia (Desmatamento)": "🔴 Alta para média de 11.403 km²/ano",
            "Segurança (Homicídios)": "⚪ Forte queda para 21,7 /100 mil - Entretanto, se deu pelo COVID"
        },
        {
            "Mandato": "Lula III (2023–2026)",
            "Crescimento do PIB": "🟢 +2,70% a.a.",
            "Inflação (IPCA)": "🟢 4,41% a.a. (menor média)",
            "Contas e Dívida (% PIB)": "🔴 Déficit -0,80% | Dívida subiu a 81,9%",
            "Emprego e Renda Real": "🟢 Menor desemprego (5,4%) | Maior salário (R$ 1.936)",
            "Social (Pobreza e Gini)": "🟢 Menor pobreza (22,4%) e menor Gini (0,504)",
            "Amazônia (Desmatamento)": "🟢 Queda de >50% (5.731 km² em 2025)",
            "Segurança (Homicídios)": "🟢 Menor taxa da série (19,8 /100 mil)"
        }
    ])
    st.dataframe(df_semaforo, use_container_width=True, hide_index=True)

# Resumo por mandato calculado para as demais abas
df_resumo = calcular_resumo_mandatos(df_filtrado, cod_indicador, meta_ind["tipo_agregacao"], col_grupo)
df_resumo["Mandato_Label_Curto"] = df_resumo["Mandato"].apply(formatar_rotulo_eixo_x)
mapa_cores_curto = {formatar_rotulo_eixo_x(k): v for k, v in mapa_cores.items()}

polaridade_badge = (
    "🟢 **Quanto MAIOR, melhor**" if meta_ind.get("polaridade") == "maior_melhor"
    else "🟠 **Quanto MENOR, melhor**" if meta_ind.get("polaridade") == "menor_melhor"
    else "🔵 **Indicador de Preço Relativo**"
)


def render_cabecalho_e_kpis() -> None:
    """Renderiza o cabeçalho explicativo e os cards com fotos redondas nas abas analíticas."""
    st.subheader(f"{icone_ind} {meta_ind['nome']} ({meta_ind['unidade']})")
    st.info(
        f"{polaridade_badge}  |  🔗 **Fonte Oficial:** [{meta_ind['fonte']}]({meta_ind['url']}) (`{meta_ind['codigo_api']}`)\n\n"
        f"**- O que este indicador significa no dia a dia?** {explicacao_leigo}\n\n"
        f"**- O que os dados mostram (2003–2026)?** {insight_geral}"
    )
    if len(df_resumo) > 0:
        pol = meta_ind.get("polaridade", "neutro")
        mandato_vencedor = None
        if pol == "maior_melhor":
            mandato_vencedor = df_resumo.loc[df_resumo["Média Anual"].idxmax(), "Mandato"]
        elif pol == "menor_melhor":
            mandato_vencedor = df_resumo.loc[df_resumo["Média Anual"].idxmin(), "Mandato"]

        cols_kpi = st.columns(len(df_resumo))
        for idx, row in df_resumo.iterrows():
            mandato_id = row["Mandato"]
            eh_vencedor = (mandato_vencedor is not None and mandato_id == mandato_vencedor)
            m_info = mapa_cfg.get(mandato_id, {})
            cor = m_info.get("cor", "#334155")
            curto = m_info.get("curto", mandato_id.split(" (")[0])
            default_f1, default_f2 = DEFAULT_FOTOS.get(mandato_id, ("", None))
            foto1 = m_info.get("foto") or default_f1
            foto2 = m_info.get("foto_extra") or default_f2

            bg_kpi = "linear-gradient(180deg, #dcfce7 0%, #ecfdf5 100%)" if eh_vencedor else "#ffffff"
            borda_kpi = "2px solid #22c55e" if eh_vencedor else "1px solid #e2e8f0"
            badge_vencedor_html = (
                '<div style="background:#16a34a; color:#ffffff; font-size:10px; font-weight:800; padding:2px 7px; border-radius:999px; display:inline-block; margin-bottom:4px; text-transform:uppercase;">🏆 Melhor Média</div>'
                if eh_vencedor else '<div style="height:18px;"></div>'
            )

            if foto2:
                imgs_html = (
                    f'<div style="display:flex; justify-content:center; align-items:center; margin-bottom:6px;">'
                    f'<img src="{foto1}" style="width:46px; height:46px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor}; margin-right:-10px; z-index:2;" />'
                    f'<img src="{foto2}" style="width:46px; height:46px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor}; z-index:1;" />'
                    f'</div>'
                )
            else:
                imgs_html = (
                    f'<img src="{foto1}" style="width:50px; height:50px; border-radius:50%; object-fit:cover; object-position:center 18%; border:2px solid {cor}; margin:0 auto 6px auto; display:block;" />'
                )

            periodo_r = row["Período"]
            resumo_r = row["Resumo Principal"]
            detalhe_r = row["Detalhe"]
            ini_r = row["Início (1º Ano)"]
            fim_r = row["Fim (Último Ano)"]
            kpi_html = (
                f'<div style="border:{borda_kpi}; border-top:4px solid {cor}; border-radius:14px; padding:10px; background:{bg_kpi}; text-align:center; box-shadow:0 1px 2px rgba(0,0,0,0.04); margin-bottom:10px;">'
                f'{badge_vencedor_html}'
                f'{imgs_html}'
                f'<div style="font-weight:800; font-size:13px; color:#0f172a;">{curto}</div>'
                f'<div style="font-size:11px; color:#64748b; margin-bottom:4px;">{periodo_r}</div>'
                f'<div style="font-weight:800; font-size:15px; color:#0f172a;">{resumo_r}</div>'
                f'<div style="font-size:11px; font-weight:600; color:#475569; margin-top:2px;">{detalhe_r}</div>'
                f'<div style="font-size:10px; color:#94a3b8; margin-top:5px; border-top:1px solid #f1f5f9; padding-top:4px;">Início: <b>{ini_r}</b> → Fim: <b>{fim_r}</b></div>'
                f'</div>'
            )
            with cols_kpi[idx]:
                st.markdown(kpi_html, unsafe_allow_html=True)


with aba1:
    render_cabecalho_e_kpis()
    c1, c2 = st.columns(2)
    with c1:
        y_vals_m = df_resumo["Média Anual"]
        y_min_m = min(0.0, float(y_vals_m.min()) * 1.28) if len(y_vals_m) else 0.0
        y_max_m = max(0.0, float(y_vals_m.max()) * 1.24) if len(y_vals_m) else 10.0

        fig_bar = px.bar(
            df_resumo,
            x="Mandato_Label_Curto",
            y="Média Anual",
            color="Mandato_Label_Curto",
            color_discrete_map=mapa_cores_curto,
            text="Média Anual",
            title=f"Média Anual por Mandato ({meta_ind['unidade']})"
        )
        fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside", cliponaxis=False)
        fig_bar.update_yaxes(title_text=None, range=[y_min_m, y_max_m])
        mostrar_grafico_plotly(fig_bar, height=440, show_legend=False)

    with c2:
        y_vals_v = df_resumo["Acumulado / Variação no Mandato"]
        y_min_v = min(0.0, float(y_vals_v.min()) * 1.28) if len(y_vals_v) else 0.0
        y_max_v = max(0.0, float(y_vals_v.max()) * 1.24) if len(y_vals_v) else 10.0

        fig_var = px.bar(
            df_resumo,
            x="Mandato_Label_Curto",
            y="Acumulado / Variação no Mandato",
            color="Mandato_Label_Curto",
            color_discrete_map=mapa_cores_curto,
            text="Acumulado / Variação no Mandato",
            title=f"Saldo / Variação Total no Mandato ({meta_ind['unidade']})"
        )
        fig_var.update_traces(texttemplate="%{text:+.2f}", textposition="outside", cliponaxis=False)
        fig_var.update_yaxes(title_text=None, range=[y_min_v, y_max_v])
        mostrar_grafico_plotly(fig_var, height=440, show_legend=False)

    st.subheader("Tabela Comparativa Detalhada por Mandato")
    cols_exibir = [c for c in df_resumo.columns if c != "Mandato_Label_Curto"]
    st.dataframe(df_resumo[cols_exibir], use_container_width=True, hide_index=True)

with aba2:
    render_cabecalho_e_kpis()
    fig_ts = go.Figure()
    for m in lista_mandatos_cfg:
        if m["id"] in mandatos_ativos:
            fig_ts.add_vrect(
                x0=m["inicio"] - 0.5,
                x1=m["fim"] + 0.5,
                fillcolor=m["cor"],
                opacity=0.10,
                line_width=0,
                annotation_text=m.get("curto", m["id"].split(" (")[0]),
                annotation_position="top left"
            )

    fig_ts.add_trace(go.Scatter(
        x=df_filtrado["ano"],
        y=df_filtrado[cod_indicador],
        mode="lines+markers+text",
        text=[f"{v:.1f}" for v in df_filtrado[cod_indicador]],
        textposition="top center",
        cliponaxis=False,
        line=dict(color="#0f172a", width=3),
        marker=dict(size=9, color=[mapa_cores.get(g, "#334155") for g in df_filtrado[col_grupo]]),
        name=meta_ind["nome"]
    ))
    fig_ts.update_layout(
        title=f"Evolução Histórica Anual (2003–2026) — {meta_ind['nome']} ({meta_ind['unidade']})",
        xaxis=dict(dtick=1)
    )
    fig_ts.update_yaxes(title_text=meta_ind["unidade"])
    mostrar_grafico_plotly(fig_ts, height=490, show_legend=False)

with aba3:
    render_cabecalho_e_kpis()
    modo_comp = st.radio(
        "Como comparar o início e o fim de cada governo?",
        options=["Valor Original (Ano 1 ao Ano 4)", "Índice Base 100 (1º Ano do Mandato = 100)"],
        horizontal=True,
        key="radio_modo_comparacao_traj"
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
        title=f"Trajetória do 1º ao 4º Ano de Governo — {meta_ind['nome']}",
        labels={"ano_mandato": "Ano do Mandato", "valor_plot": y_label, col_grupo: "Governo"}
    )
    fig_comp.update_layout(xaxis=dict(dtick=1, tickvals=[1, 2, 3, 4], ticktext=["1º Ano", "2º Ano", "3º Ano", "4º Ano"]))
    fig_comp.update_yaxes(title_text=y_label)
    mostrar_grafico_plotly(fig_comp, height=490, show_legend=True)

with aba4:
    st.subheader("Catálogo de Fontes Oficiais e Download da Base (2003–2026)")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Baixar Base Consolidada Completa (CSV)",
        data=csv_bytes,
        file_name="dados_socioeconomicos_brasil_2003_2026.csv",
        mime="text/csv",
        key="btn_download_csv_base"
    )
    df_catalogo = pd.DataFrame([
        {
            "Tema": v["eixo"],
            "Indicador": f"{get_icone(k)} {v['nome']}",
            "Unidade": v["unidade"],
            "O que significa": get_explicacao_leigo(k),
            "Série / Tabela API": v["codigo_api"],
            "Fonte Oficial": v["fonte"],
            "URL Oficial": v["url"]
        }
        for k, v in INDICADORES.items()
    ])
    st.dataframe(df_catalogo, use_container_width=True, hide_index=True)

# Impede execução duplicada caso o código seja colado duas vezes no mesmo arquivo
st.stop()