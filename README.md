# Observatório Socioeconômico dos Mandatos Presidenciais no Brasil (2003–2026)

Aplicação em **Streamlit** + **Plotly** para análise comparativa de 20 indicadores oficiais distribuídos em **8 eixos temáticos** (Macroeconomia, Fiscal e Dívida, Trabalho e Renda, Social e Desigualdade, Educação, Saúde, Segurança Pública e Meio Ambiente / Setor Externo) ao longo dos mandatos presidenciais de **Lula I (2003–2006)** a **Lula III (2023–2026)**.

## Como Executar Localmente

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie o servidor do Streamlit:
   ```bash
   streamlit run app.py
   ```

## Estrutura do Projeto

- `app.py`: Interface principal em Streamlit com 4 abas analíticas e seletor dinâmico para unificar ou separar o ciclo 2015–2018 (Dilma II e Michel Temer).
- `src/config.py`: Dicionário de mandatos, metadados metodológicos, polaridade e códigos oficiais das APIs abertas.
- `src/etl_apis.py`: Funções de extração direta via API REST no SGS do Banco Central, API v3 Agregados/SIDRA do IBGE e API OData4 do Ipeadata.
- `src/metrics.py`: Cálculo de taxas geométricas compostas (PIB e IPCA), somas acumuladas de fluxo (Balança Comercial e Desmatamento PRODES) e variações de estoque (Dívida/PIB, Desemprego, Gini, IDEB, Saúde e Homicídios).
- `data/dados_socioeconomicos_brasil_2003_2026.csv`: Base histórica anual consolidada e pronta para uso imediato.
