# -*- coding: utf-8 -*-
"""
Configurações de mandatos presidenciais (2003-2026), paleta visual e catálogo de indicadores.
"""

MANDATOS_CICLO = [
    {"id": "Lula I (2003–2006)", "presidente": "Luiz Inácio Lula da Silva", "inicio": 2003, "fim": 2006, "cor": "#dc2626"},
    {"id": "Lula II (2007–2010)", "presidente": "Luiz Inácio Lula da Silva", "inicio": 2007, "fim": 2010, "cor": "#b91c1c"},
    {"id": "Dilma I (2011–2014)", "presidente": "Dilma Rousseff", "inicio": 2011, "fim": 2014, "cor": "#ea580c"},
    {"id": "Dilma II / Temer (2015–2018)", "presidente": "Dilma Rousseff / Michel Temer", "inicio": 2015, "fim": 2018, "cor": "#7c3aed"},
    {"id": "Bolsonaro (2019–2022)", "presidente": "Jair Bolsonaro", "inicio": 2019, "fim": 2022, "cor": "#2563eb"},
    {"id": "Lula III (2023–2026)", "presidente": "Luiz Inácio Lula da Silva", "inicio": 2023, "fim": 2026, "cor": "#059669"},
]

MANDATOS_SEPARADOS = [
    {"id": "Lula I (2003–2006)", "presidente": "Luiz Inácio Lula da Silva", "inicio": 2003, "fim": 2006, "cor": "#dc2626"},
    {"id": "Lula II (2007–2010)", "presidente": "Luiz Inácio Lula da Silva", "inicio": 2007, "fim": 2010, "cor": "#b91c1c"},
    {"id": "Dilma I (2011–2014)", "presidente": "Dilma Rousseff", "inicio": 2011, "fim": 2014, "cor": "#ea580c"},
    {"id": "Dilma II (2015–2016)", "presidente": "Dilma Rousseff", "inicio": 2015, "fim": 2016, "cor": "#d97706"},
    {"id": "Temer (2016–2018)", "presidente": "Michel Temer", "inicio": 2017, "fim": 2018, "cor": "#0284c7"},
    {"id": "Bolsonaro (2019–2022)", "presidente": "Jair Bolsonaro", "inicio": 2019, "fim": 2022, "cor": "#2563eb"},
    {"id": "Lula III (2023–2026)", "presidente": "Luiz Inácio Lula da Silva", "inicio": 2023, "fim": 2026, "cor": "#059669"},
]

INDICADORES = {
    "pib_cresc_aa": {
        "nome": "Crescimento do PIB Real",
        "eixo": "Macroeconomia",
        "unidade": "% a.a.",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "taxa_composta",
        "fonte": "IBGE – Sistema de Contas Nacionais Trimestrais (Tabela SIDRA 5932 / SGS 7326)",
        "url": "https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9300-contas-nacionais",
        "codigo_api": "SGS 7326 / SIDRA 5932",
        "descricao": "Variação percentual anual do Produto Interno Bruto a preços constantes."
    },
    "ipca_aa": {
        "nome": "Inflação Oficial (IPCA)",
        "eixo": "Macroeconomia",
        "unidade": "% a.a.",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "taxa_composta",
        "fonte": "IBGE / Banco Central do Brasil (Série SGS 433)",
        "url": "https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarSeries&series=433",
        "codigo_api": "SGS 433 / SIDRA 1737",
        "descricao": "Índice Nacional de Preços ao Consumidor Amplo acumulado em 12 meses."
    },
    "selic_meta_fim": {
        "nome": "Taxa Básica de Juros (Selic Meta)",
        "eixo": "Macroeconomia",
        "unidade": "% a.a.",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "Banco Central do Brasil (Série SGS 432 / 11)",
        "url": "https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic",
        "codigo_api": "SGS 432",
        "descricao": "Meta para a taxa Selic definida pelo COPOM ao final de cada ano."
    },
    "cambio_medio": {
        "nome": "Taxa de Câmbio Nominal (PTAX)",
        "eixo": "Macroeconomia",
        "unidade": "R$ / US$",
        "polaridade": "neutro",
        "tipo_agregacao": "estoque_fim",
        "fonte": "Banco Central do Brasil (Série SGS 3698)",
        "url": "https://www3.bcb.gov.br/sgspub/",
        "codigo_api": "SGS 3698",
        "descricao": "Taxa média anual de câmbio livre (R$/US$ venda)."
    },
    "divida_bruta_pib": {
        "nome": "Dívida Bruta do Governo Geral (DBGG)",
        "eixo": "Fiscal e Dívida",
        "unidade": "% do PIB",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "Banco Central do Brasil (Série SGS 13762)",
        "url": "https://www.bcb.gov.br/estatisticas/estatisticasfiscais",
        "codigo_api": "SGS 13762",
        "descricao": "Dívida Bruta do Governo Geral (Governo Federal, INSS, Estados e Municípios) em proporção ao PIB."
    },
    "divida_liquida_pib": {
        "nome": "Dívida Líquida do Setor Público (DLSP)",
        "eixo": "Fiscal e Dívida",
        "unidade": "% do PIB",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "Banco Central do Brasil (Série SGS 4513)",
        "url": "https://dadosabertos.bcb.gov.br/dataset/4513-divida-liquida-do-setor-publico--pib---total---setor-publico-consolidado/resource/3337fe4f-a3c6-4a68-94e6-aa099e4607c0",
        "codigo_api": "SGS 4513",
        "descricao": "Dívida Líquida do Setor Público Consolidado como proporção do PIB."
    },
    "resultado_primario_pib": {
        "nome": "Resultado Primário do Setor Público",
        "eixo": "Fiscal e Dívida",
        "unidade": "% do PIB",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "fluxo_media",
        "fonte": "Tesouro Transparente (RTN CKAN) e Banco Central",
        "url": "https://www.tesourotransparente.gov.br/temas/estatisticas-fiscais-e-planejamento/resultado-do-tesouro-nacional-rtn-conteudos-relacionados",
        "codigo_api": "Tesouro CKAN / SGS 5793",
        "descricao": "Superávit (+) ou déficit (-) primário anual consolidado em % do PIB."
    },
    "desemprego_medio": {
        "nome": "Taxa Média de Desocupação (Desemprego)",
        "eixo": "Trabalho e Renda",
        "unidade": "%",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IBGE – PNAD Contínua (Tabela SIDRA 4099) e PME harmonizada via Ipeadata",
        "url": "https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pesquisa-nacional-por-amostra-de-domicilios-continua-trimestral.html",
        "codigo_api": "SIDRA 4099 / Ipeadata",
        "descricao": "Percentual médio anual da força de trabalho desocupada."
    },
    "salario_minimo_real_2026": {
        "nome": "Salário Mínimo Real (Preços de 2026)",
        "eixo": "Trabalho e Renda",
        "unidade": "R$ (2026)",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "Ipeadata (GAC12_SALMINRE12) e BCB (SGS 1619) deflacionado pelo IPCA",
        "url": "https://www.ipea.gov.br/portal/categorias/2-uncategorised/1825-api",
        "codigo_api": "Ipea GAC12_SALMINRE12",
        "descricao": "Poder de compra real do salário mínimo nacional em reais constantes de 2026."
    },
    "gini_renda": {
        "nome": "Índice de Gini da Renda Domiciliar",
        "eixo": "Social e Desigualdade",
        "unidade": "Índice (0–1)",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IBGE – Síntese de Indicadores Sociais / PNAD Contínua e Banco Mundial",
        "url": "https://pypi.org/project/wbgapi/",
        "codigo_api": "SIDRA 7435 / WBG SI.POV.GINI",
        "descricao": "Mede a concentração de renda domiciliar per capita (quanto mais próximo de 0, menor a desigualdade)."
    },
    "taxa_pobreza_pct": {
        "nome": "Taxa de Pobreza Monetária",
        "eixo": "Social e Desigualdade",
        "unidade": "% da pop.",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IBGE (Síntese de Indicadores Sociais) e Ipeadata",
        "url": "https://www.ipeadata.gov.br/",
        "codigo_api": "IBGE SIS / WBG SI.POV.UMIC",
        "descricao": "Proporção da população abaixo da linha de pobreza monetária (critério Banco Mundial / IBGE)."
    },
    "ideb_anos_iniciais": {
        "nome": "IDEB – Ensino Fundamental (Anos Iniciais)",
        "eixo": "Educação",
        "unidade": "Nota (0–10)",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "INEP – Índice de Desenvolvimento da Educação Básica",
        "url": "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb",
        "codigo_api": "INEP IDEB / Base dos Dados",
        "descricao": "Indicador nacional de qualidade educacional nos anos iniciais (1º ao 5º ano)."
    },
    "ideb_ensino_medio": {
        "nome": "IDEB – Ensino Médio",
        "eixo": "Educação",
        "unidade": "Nota (0–10)",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "INEP – Índice de Desenvolvimento da Educação Básica",
        "url": "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb",
        "codigo_api": "INEP IDEB / Base dos Dados",
        "descricao": "Indicador nacional de qualidade educacional no Ensino Médio."
    },
    "taxa_analfabetismo_15m": {
        "nome": "Taxa de Analfabetismo (15 anos ou mais)",
        "eixo": "Educação",
        "unidade": "%",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IBGE – PNAD Contínua Educação / Censo Demográfico",
        "url": "https://www.ibge.gov.br/estatisticas/sociais/trabalho/17270-pnad-continua.html",
        "codigo_api": "SIDRA 7113",
        "descricao": "Percentual da população de 15 anos ou mais que não sabe ler e escrever."
    },
    "mortalidade_infantil_mil": {
        "nome": "Taxa de Mortalidade Infantil",
        "eixo": "Saúde",
        "unidade": "por mil nasc. vivos",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IBGE – Tábuas Completas de Mortalidade e SIM/DATASUS",
        "url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9126-tabuas-completas-de-mortalidade.html",
        "codigo_api": "IBGE Tábuas / DATASUS MRT.1.01",
        "descricao": "Óbitos de menores de 1 ano para cada mil nascidos vivos."
    },
    "expectativa_vida_anos": {
        "nome": "Expectativa de Vida ao Nascer",
        "eixo": "Saúde",
        "unidade": "Anos",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IBGE – Tábuas Completas de Mortalidade",
        "url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9126-tabuas-completas-de-mortalidade.html",
        "codigo_api": "IBGE Tábuas de Mortalidade",
        "descricao": "Esperança de vida média ao nascer da população brasileira (impactada em 2020-2021 pela COVID-19)."
    },
    "taxa_homicidios_100m": {
        "nome": "Taxa de Homicídios por 100 mil hab.",
        "eixo": "Segurança Pública",
        "unidade": "por 100 mil hab.",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "IPEA e Fórum Brasileiro de Segurança Pública – Atlas da Violência (SIM/DATASUS)",
        "url": "https://www.ipea.gov.br/atlasviolencia/dados-series/20/",
        "codigo_api": "Atlas da Violência Série 20",
        "descricao": "Taxa anual de homicídios registrados por 100 mil habitantes no Brasil."
    },
    "desmatamento_amazonia_km2": {
        "nome": "Desmatamento na Amazônia Legal (PRODES)",
        "eixo": "Meio Ambiente",
        "unidade": "km²/ano",
        "polaridade": "menor_melhor",
        "tipo_agregacao": "fluxo_soma",
        "fonte": "INPE – Projeto PRODES / Plataforma TerraBrasilis",
        "url": "https://terrabrasilis.dpi.inpe.br/app/dashboard/deforestation/biomes/legal_amazon/increments",
        "codigo_api": "TerraBrasilis PRODES ALB",
        "descricao": "Incremento anual de área desmatada por corte raso na Amazônia Legal Brasileira (km²)."
    },
    "saldo_comercial_us_bi": {
        "nome": "Saldo da Balança Comercial",
        "eixo": "Balança Comercial e Setor Externo",
        "unidade": "US$ bilhões",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "fluxo_soma",
        "fonte": "MDIC – Sistema Comex Stat / Estatísticas de Comércio Exterior",
        "url": "https://comexstat.mdic.gov.br/pt/geral",
        "codigo_api": "MDIC Comex Stat / SGS 22707",
        "descricao": "Superávit (+) ou déficit (-) anual da balança comercial brasileira (Exportações FOB menos Importações FOB)."
    },
    "reservas_internacionais_us_bi": {
        "nome": "Reservas Internacionais (Conceito Liquidez)",
        "eixo": "Balança Comercial e Setor Externo",
        "unidade": "US$ bilhões",
        "polaridade": "maior_melhor",
        "tipo_agregacao": "estoque_fim",
        "fonte": "Banco Central do Brasil – Estatísticas do Setor Externo (Série SGS 13621)",
        "url": "https://www.bcb.gov.br/estatisticas/estatisticassetorexterno",
        "codigo_api": "SGS 13621",
        "descricao": "Estoque de reservas internacionais brasileiras ao final de cada ano em US$ bilhões."
    }
}
