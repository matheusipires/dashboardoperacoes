import streamlit as st

# ✅ Precisa estar antes de qualquer outra coisa do Streamlit
st.set_page_config(page_title="Painel Sistemas", layout="wide")

# Agora os outros imports
import os
import sys
import pandas as pd
import numpy as np
import base64
import plotly.graph_objects as go


# ✅ Precisa ser o primeiro comando do Streamlit
st.set_page_config(page_title="Dashboard OS", layout="wide")

# ✅ Gera logo em base64
def get_logo_base64():
    with open("app/assets/logo.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"

logo_base64 = get_logo_base64()

# ✅ Carrega e injeta HTML do cabeçalho com logo embutido
with open("app/styles/components.html", encoding="utf-8") as f:
    html = f.read().format(logo_base64=logo_base64)
    st.markdown(html, unsafe_allow_html=True)

# ✅ Carrega o CSS externo
with open("app/styles/layout.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# (continue com o restante do seu código aqui...)

COR_AZUL = '#1B556B'
COR_LARANJA = '#E98C5F'
COR_VERDE = '#32AF9D'

with st.spinner("Carregando dados..."):

    df = carregar_dados()

    df = df[df['CLIENTE'].notna() & (df['CLIENTE'].str.strip() != "-")]
    
# ✅ Filtros fora da sidebar: Período
st.markdown("### 📆 Selecione o Período de Abertura")
data_min = df['Abertura'].min().date()
data_max = df['Abertura'].max().date()
intervalo = st.date_input(
    "Período de abertura:",
    [data_min, data_max],
    min_value=data_min,
    max_value=data_max
)

# Verifica se o usuário selecionou duas datas
if len(intervalo) != 2:
    st.warning("⚠️ Por favor, selecione um **intervalo válido** com data de início e fim.")
    st.stop()

data_inicio, data_fim = intervalo

# ✅ Filtros na sidebar
with st.sidebar:
    st.header("🔎 Filtros")
    with st.expander("🎯 Selecione os filtros"):

        # Filtro CLIENTE
        clientes = sorted(df['CLIENTE'].dropna().unique())
        todos_clientes = st.checkbox("Selecionar todos os clientes", value=True)
        clientes_selecionados = clientes if todos_clientes else st.multiselect("Unidade", clientes)

        # Filtro TIPO DE MANUTENÇÃO2
        tipos = sorted(df['TIPO DE MANUTENÇÃO2'].dropna().unique())
        todos_tipos = st.checkbox("Selecionar todos os tipos de manutenção", value=True)
        tipos_selecionados = tipos if todos_tipos else st.multiselect("Tipo de manutenção", tipos)

        # Filtro SUPERVISOR
        supervisores = sorted(df['SUPERVISOR'].dropna().unique())
        todos_supervisores = st.checkbox("Todos os supervisores", value=True)
        supervisores_selecionados = supervisores if todos_supervisores else st.multiselect("Supervisor", supervisores)

        # Filtro COORDENADOR
        coordenadores = sorted(df['COORDENADOR'].dropna().unique())
        todos_coordenadores = st.checkbox("Todos os coordenadores", value=True)
        coordenadores_selecionados = coordenadores if todos_coordenadores else st.multiselect("Coordenador", coordenadores)

        # Filtro REGIÃO
        regioes = sorted(df['REGIÃO'].dropna().unique())
        todas_regioes = st.checkbox("Todas as regiões", value=True)
        regioes_selecionadas = regioes if todas_regioes else st.multiselect("Região", regioes)

        # Filtro CIDADE
        cidades = sorted(df['CIDADE'].dropna().unique())
        todas_cidades = st.checkbox("Todas as cidades", value=True)
        cidades_selecionadas = cidades if todas_cidades else st.multiselect("Cidade", cidades)

        # Filtro GRUPO
        grupos = sorted(df['GRUPO'].dropna().unique())
        todos_grupos = st.checkbox("Todos os grupos", value=True)
        grupos_selecionados = grupos if todos_grupos else st.multiselect("Grupo", grupos)

    # ✅ Mostrar filtros ativos
    with st.expander("📌 Filtros Selecionados"):
        st.markdown(f"""
        - **Clientes:** {', '.join(clientes_selecionados)}
        - **Tipos de manutenção:** {', '.join(tipos_selecionados)}
        - **Supervisores:** {', '.join(supervisores_selecionados)}
        - **Coordenadores:** {', '.join(coordenadores_selecionados)}
        - **Regiões:** {', '.join(regioes_selecionadas)}
        - **Cidades:** {', '.join(cidades_selecionadas)}
        - **Grupos:** {', '.join(grupos_selecionados)}
        """)

st.markdown(
    f"🗓️ Intervalo selecionado: **{data_inicio.strftime('%d/%m/%Y')}** até **{data_fim.strftime('%d/%m/%Y')}**"
)

df_filtrado = df[
    (df['CLIENTE'].isin(clientes_selecionados)) &
    (df['TIPO DE MANUTENÇÃO2'].isin(tipos_selecionados)) &
    (df['SUPERVISOR'].isin(supervisores_selecionados)) &
    (df['COORDENADOR'].isin(coordenadores_selecionados)) &
    (df['REGIÃO'].isin(regioes_selecionadas)) &
    (df['CIDADE'].isin(cidades_selecionadas)) &
    (df['GRUPO'].isin(grupos_selecionados)) &
    (df['Abertura'].dt.date >= data_inicio) &
    (df['Abertura'].dt.date <= data_fim)
].copy()



situacoes = df_filtrado['SITUAÇÃO OS'].str.lower().str.strip()

from urllib.parse import urlencode

# Configurações iniciais
st.set_page_config(page_title="Painel Sistemas", layout="wide")

# 🔙 Botão para voltar ao painel principal
params = urlencode({"painel": "principal"})
st.markdown(f"""
    <a href="/" target="_self">
        <button style="margin-top: 20px; padding: 0.6rem 1.2rem; background-color: #E98C5F; color: white; border: none; border-radius: 5px; font-size: 1rem;">
            Voltar ao Painel Principal
        </button>
    </a>
""", unsafe_allow_html=True)

# Aqui seguem os filtros e gráficos do painel de sistemas


    # Cards
# 🔄 Atualiza valores com mesma lógica dos gráficos
df_validas = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente', 'Fechada'])].copy()
total_os = len(df_validas)

# Pendentes = Aberta + Pendente
pendentes_total = df_validas[df_validas['SITUAÇÃO OS'].isin(['Aberta', 'Pendente'])].shape[0]

# Concluídas no mesmo mês da abertura
df_validas['Mes_Abertura'] = df_validas['Abertura'].dt.to_period('M')
df_validas['Mes_Fechamento'] = df_validas['Fechamento'].dt.to_period('M')
concluidas_mesmo_mes = df_validas[
    (df_validas['SITUAÇÃO OS'] == 'Fechada') &
    (df_validas['Mes_Abertura'] == df_validas['Mes_Fechamento'])
].shape[0]

# % Conclusão
taxa = f"{(concluidas_mesmo_mes / total_os * 100) if total_os > 0 else 0:.1f}%".replace('.', ',')

# 🔤 Cards
st.markdown(f"""
<div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
    <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #1B556B, #3e7c91); padding: 1rem; border-radius: 10px; color: white; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 0.9rem;">🔧 Total de OS</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{total_os}</div>
    </div>
    <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #ffc107, #ffcd39); padding: 1rem; border-radius: 10px; color: #333; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 0.9rem;">⚠️ Pendentes</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{pendentes_total}</div>
    </div>
    <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #28a745, #5cd081); padding: 1rem; border-radius: 10px; color: white; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 0.9rem;">✅ Concluídas (mesmo mês)</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{concluidas_mesmo_mes}</div>
    </div>
    <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #6c757d, #adb5bd); padding: 1rem; border-radius: 10px; color: white; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 0.9rem;">📈 % Conclusão</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{taxa}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# 📊 KPI - Acompanhamento de Abertura e Fechamento de OS por Mês

# Filtra somente OS válidas para o gráfico
df_total = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente', 'Fechada'])].copy()
df_total['Mes_Ano'] = df_total['Abertura'].dt.to_period('M').astype(str)  # formato '2025-01'

df_fechadas_mesmo_mes = df_filtrado[
    (df_filtrado['SITUAÇÃO OS'] == 'Fechada') &
    (df_filtrado['Fechamento'].notna()) &
    (df_filtrado['Abertura'].dt.to_period('M') == df_filtrado['Fechamento'].dt.to_period('M'))
].copy()
df_fechadas_mesmo_mes['Mes_Ano'] = df_fechadas_mesmo_mes['Abertura'].dt.to_period('M').astype(str)

# Agrupamentos
grupo_total = df_total.groupby('Mes_Ano')['OS'].count().reset_index(name='Total')
grupo_fechadas = df_fechadas_mesmo_mes.groupby('Mes_Ano')['OS'].count().reset_index(name='Fechadas')
grupo_mes = grupo_total.merge(grupo_fechadas, on='Mes_Ano', how='left').fillna(0)
grupo_mes['% Conclusão'] = (grupo_mes['Fechadas'] / grupo_mes['Total']) * 100

# Conversão para ordenação correta
grupo_mes['Mes_Ano_Date'] = pd.to_datetime(grupo_mes['Mes_Ano'], format='%Y-%m')
grupo_final_sorted = grupo_mes.sort_values('Mes_Ano_Date').reset_index(drop=True)
grupo_final_sorted['Mes_Ano_Formatado'] = grupo_final_sorted['Mes_Ano_Date'].dt.strftime('%b/%y').str.capitalize()

# Gráfico KPI
st.markdown("### 📊 KPI - Acompanhamento de Abertura e Fechamento de OS por Mês")
fig_kpi = grafico_kpi(grupo_final_sorted, COR_AZUL, COR_VERDE, COR_LARANJA)
st.plotly_chart(fig_kpi, use_container_width=True)

# Gráfico de Evolução
fig_evolucao = grafico_evolucao(grupo_final_sorted, COR_AZUL, COR_LARANJA)
st.plotly_chart(fig_evolucao, use_container_width=True)


st.markdown("### 🏆 Rankings de % Conclusão")

opcao_ranking = st.radio("Escolha o tipo de ranking:", ["Por Cliente", "Por Tipo de Manutenção"], horizontal=True)

# Criar colunas auxiliares
df_filtrado['Mes_Abertura'] = df_filtrado['Abertura'].dt.to_period('M').astype(str)
df_filtrado['Mes_Fechamento'] = df_filtrado['Fechamento'].dt.to_period('M').astype(str)
df_validas = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente', 'Fechada'])].copy()

if opcao_ranking == "Por Cliente":
    # Total de OS por cliente
    total_os = df_validas.groupby('CLIENTE')['OS'].count().reset_index(name='Abertas')

    # Fechadas dentro do mesmo mês da abertura
    df_fechadas = df_validas[
        (df_validas['SITUAÇÃO OS'] == 'Fechada') &
        (df_validas['Mes_Abertura'] == df_validas['Mes_Fechamento'])
    ]
    fechadas = df_fechadas.groupby('CLIENTE')['OS'].count().reset_index(name='Fechadas')

    # Juntar e calcular ranking
    ranking = pd.merge(total_os, fechadas, on='CLIENTE', how='left').fillna(0)
    ranking['% Conclusão'] = (ranking['Fechadas'] / ranking['Abertas']) * 100
    ranking = ranking.sort_values(by='% Conclusão', ascending=False).reset_index(drop=True)
    ranking['Classificação'] = ranking.index + 1
    ranking['% Conclusão'] = ranking['% Conclusão'].round(1).astype(str) + '%'

    st.dataframe(
        ranking[['Classificação', 'CLIENTE', 'Abertas', 'Fechadas', '% Conclusão']],
        use_container_width=True,
        hide_index=True
    )

elif opcao_ranking == "Por Tipo de Manutenção":
    total_tipo = df_validas.groupby('TIPO DE MANUTENÇÃO2')['OS'].count().reset_index(name='Abertas')

    df_fechadas_tipo = df_validas[
        (df_validas['SITUAÇÃO OS'] == 'Fechada') &
        (df_validas['Mes_Abertura'] == df_validas['Mes_Fechamento'])
    ]
    fechadas_tipo = df_fechadas_tipo.groupby('TIPO DE MANUTENÇÃO2')['OS'].count().reset_index(name='Fechadas')

    ranking_tipo = pd.merge(total_tipo, fechadas_tipo, on='TIPO DE MANUTENÇÃO2', how='left').fillna(0)
    ranking_tipo['% Conclusão'] = (ranking_tipo['Fechadas'] / ranking_tipo['Abertas']) * 100
    ranking_tipo = ranking_tipo.sort_values(by='% Conclusão', ascending=False).reset_index(drop=True)
    ranking_tipo['Classificação'] = ranking_tipo.index + 1
    ranking_tipo['% Conclusão'] = ranking_tipo['% Conclusão'].round(1).astype(str) + '%'

    st.dataframe(
        ranking_tipo[['Classificação', 'TIPO DE MANUTENÇÃO2', 'Abertas', 'Fechadas', '% Conclusão']],
        use_container_width=True,
        hide_index=True
    )


