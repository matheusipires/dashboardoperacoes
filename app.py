try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    from scripts.leitura_dados import carregar_dados
    from components.graficos import grafico_kpi, grafico_evolucao
    from urllib.parse import urlencode
    import base64
    import locale
except Exception as e:
    st.error(f"❌ Erro ao carregar bibliotecas: {e}")
    raise e


# ✅ Precisa ser o primeiro comando do Streamlit
st.set_page_config(page_title="Dashboard OS", layout="wide")

# ✅ Gera logo em base64
def get_logo_base64():
    with open("assets/logo.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"

logo_base64 = get_logo_base64()

# ✅ Carrega e injeta HTML do cabeçalho com logo embutido
with open("styles/components.html", encoding="utf-8") as f:
    html = f.read().format(logo_base64=logo_base64)
    st.markdown(html, unsafe_allow_html=True)


# ✅ Carrega o CSS externo
with open("styles/layout.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# (continue com o restante do seu código aqui...)

COR_AZUL = '#1B556B'
COR_LARANJA = '#E98C5F'
COR_VERDE = '#32AF9D'

with st.spinner("Carregando dados..."):

    df = carregar_dados()

    df = df[df['CLIENTE'].notna() & (df['CLIENTE'].str.strip() != "-")]

    # 🕒 Obtém a data mais recente da coluna 'Abertura'
data_ultima_atualizacao = df['Abertura'].max().date()

# Exibe a data de atualização no topo do painel
st.markdown(
    f"<div style='font-size:0.95rem; color:#444; margin-bottom:1rem;'>🕒 <strong>Dados atualizados até:</strong> {data_ultima_atualizacao.strftime('%d/%m/%Y')}</div>",
    unsafe_allow_html=True
)
    
# ✅ Filtros fora da sidebar: Período
with st.expander("📆 Selecione o Período de Abertura", expanded=True):

    # Intervalo de datas
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

st.markdown("""
<hr style="margin-top:2rem; margin-bottom:1rem;">
<h4 style='margin-bottom:0.5rem;'>⚙️ Selecione o tipo de métrica para análise</h4>
""", unsafe_allow_html=True)

opcao_metrica = st.radio(
    "Escolha a métrica:",
    ["Fechadas no mesmo mês da abertura", "Todas as OS fechadas"],
    horizontal=True
)



situacoes = df_filtrado['SITUAÇÃO OS'].str.lower().str.strip()

  # Cards
# 🔄 Atualiza valores com mesma lógica dos gráficos
df_validas = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente', 'Fechada'])].copy()
total_os = len(df_validas)

# Pendentes = Aberta + Pendente
pendentes_total = df_validas[df_validas['SITUAÇÃO OS'].isin(['Aberta', 'Pendente'])].shape[0]

# Concluídas no mesmo mês da abertura
df_validas = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente', 'Fechada'])].copy()
total_os = len(df_validas)

pendentes_total = df_validas[df_validas['SITUAÇÃO OS'].isin(['Aberta', 'Pendente'])].shape[0]

df_validas['Mes_Abertura'] = df_validas['Abertura'].dt.to_period('M')
df_validas['Mes_Fechamento'] = df_validas['Fechamento'].dt.to_period('M')

if opcao_metrica == "Fechadas no mesmo mês da abertura":
    concluidas = df_validas[
        (df_validas['SITUAÇÃO OS'] == 'Fechada') &
        (df_validas['Mes_Abertura'] == df_validas['Mes_Fechamento'])
    ].shape[0]
else:
    concluidas = df_validas[df_validas['SITUAÇÃO OS'] == 'Fechada'].shape[0]

taxa = f"{(concluidas / total_os * 100) if total_os > 0 else 0:.1f}%".replace('.', ',')


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
        <div style="font-size: 0.9rem;">✅ Concluídas</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{concluidas}</div>
    </div>
    <div style="flex: 1; min-width: 180px; background: linear-gradient(135deg, #6c757d, #adb5bd); padding: 1rem; border-radius: 10px; color: white; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 0.9rem;">📈 % Conclusão</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{taxa}</div>
    </div>
</div>
""", unsafe_allow_html=True)



# 📊 KPI - Acompanhamento de Abertura e Fechamento de OS por Mês

df_total = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente', 'Fechada'])].copy()
df_total['Mes_Abertura'] = df_total['Abertura'].dt.to_period('M')
df_total['Mes_Fechamento'] = df_total['Fechamento'].dt.to_period('M')
df_total['Mes_Ano'] = df_total['Abertura'].dt.to_period('M').astype(str)  # Ex: '2025-01'

# Define as OS fechadas de acordo com a métrica
if opcao_metrica == "Fechadas no mesmo mês da abertura":
    df_fechadas_grafico = df_total[
        (df_total['SITUAÇÃO OS'] == 'Fechada') &
        (df_total['Mes_Abertura'] == df_total['Mes_Fechamento'])
    ]
else:
    df_fechadas_grafico = df_total[df_total['SITUAÇÃO OS'] == 'Fechada']

# Evita o SettingWithCopyWarning
df_fechadas_grafico = df_fechadas_grafico.copy()
df_fechadas_grafico.loc[:, 'Mes_Ano'] = df_fechadas_grafico['Abertura'].dt.to_period('M').astype(str)

# Agrupamentos
grupo_total = df_total.groupby('Mes_Ano')['OS'].count().reset_index(name='Total')
grupo_fechadas = df_fechadas_grafico.groupby('Mes_Ano')['OS'].count().reset_index(name='Fechadas')

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

    if opcao_metrica == "Fechadas no mesmo mês da abertura":
        df_fechadas = df_validas[
            (df_validas['SITUAÇÃO OS'] == 'Fechada') &
            (df_validas['Mes_Abertura'] == df_validas['Mes_Fechamento'])
        ]
    else:
        df_fechadas = df_validas[df_validas['SITUAÇÃO OS'] == 'Fechada']

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

    if opcao_metrica == "Fechadas no mesmo mês da abertura":
        df_fechadas_tipo = df_validas[
            (df_validas['SITUAÇÃO OS'] == 'Fechada') &
            (df_validas['Mes_Abertura'] == df_validas['Mes_Fechamento'])
        ]
    else:
        df_fechadas_tipo = df_validas[df_validas['SITUAÇÃO OS'] == 'Fechada']

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
st.markdown("### ⏱️ Tempo Médio de Atendimento por Mês (com tendência de melhoria)")

# Filtra apenas OS com data de fechamento válida
df_duracao = df_filtrado[df_filtrado['Fechamento'].notna()].copy()
df_duracao['Tempo (dias)'] = (df_duracao['Fechamento'] - df_duracao['Abertura']).dt.days

# Agrupa por mês de abertura
df_duracao['Mes_Ano'] = df_duracao['Abertura'].dt.to_period('M').astype(str)
media_mensal = df_duracao.groupby('Mes_Ano')['Tempo (dias)'].mean().reset_index()
media_mensal['Tempo (dias)'] = media_mensal['Tempo (dias)'].round(1)

# Ordena para exibição correta no eixo X
media_mensal['Mes_Ano_Data'] = pd.to_datetime(media_mensal['Mes_Ano'], format='%Y-%m')
media_mensal = media_mensal.sort_values('Mes_Ano_Data')

# Agora gera gráfico com cores conforme tendência
import plotly.graph_objects as go

x = media_mensal['Mes_Ano'].tolist()
y = media_mensal['Tempo (dias)'].tolist()

fig_tempo = go.Figure()

for i in range(len(x) - 1):
    cor = "#28a745" if y[i+1] < y[i] else "#dc3545"  # verde se caiu, vermelho se subiu
    fig_tempo.add_trace(go.Scatter(
        x=[x[i], x[i+1]],
        y=[y[i], y[i+1]],
        mode='lines+markers+text',
        line=dict(color=cor, width=3),
        marker=dict(size=8),
        text=[f"{y[i]}", f"{y[i+1]}"],
        textposition="top center",
        showlegend=False
    ))

fig_tempo.update_layout(
    height=450,
    xaxis_title="Mês de Abertura",
    yaxis_title="Tempo Médio (dias)",
    title="Tempo Médio de Atendimento com Indicador de Tendência",
    margin=dict(l=20, r=20, t=50, b=60),
    xaxis_tickangle=-45
)

st.plotly_chart(fig_tempo, use_container_width=True)




st.markdown("### 🧾 Ranking de Problemas Recorrentes")

# Abas de seleção
opcao_problema = st.radio(
    "Escolha o tipo de problema para visualizar:",
    ["Por Causa", "Por Ocorrência"],
    horizontal=True
)

# Função com estilo condicional
def gerar_ranking_problemas(serie, titulo_coluna):
    import pandas as pd

    serie_limpa = serie.dropna().astype(str).str.strip().str.lower()
    contagem = serie_limpa.value_counts().reset_index()
    contagem.columns = [titulo_coluna, "Frequência"]

    total = contagem["Frequência"].sum()
    contagem["% do Total"] = (contagem["Frequência"] / total * 100).round(1)
    contagem["Classificação"] = contagem.index + 1

    df_resultado = contagem[["Classificação", titulo_coluna, "Frequência", "% do Total"]].copy()
    df_resultado["% do Total"] = df_resultado["% do Total"].astype(str) + "%"

    def estilo_porcentagem(val):
        num = float(val.replace("%", ""))
        if num >= 10:
            return "color: green; font-weight: bold;"
        else:
            return "color: #888;"

    styled_df = df_resultado.style.applymap(estilo_porcentagem, subset=["% do Total"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Aplica a função conforme a aba selecionada
if opcao_problema == "Por Causa":
    if 'CAUSA' in df_filtrado.columns:
        gerar_ranking_problemas(df_filtrado['CAUSA'], "Causa")
    else:
        st.warning("⚠️ Coluna 'CAUSA' não encontrada no DataFrame.")
elif opcao_problema == "Por Ocorrência":
    if 'OCORRÊNCIA' in df_filtrado.columns:
        gerar_ranking_problemas(df_filtrado['OCORRÊNCIA'], "Ocorrência")
    else:
        st.warning("⚠️ Coluna 'OCORRÊNCIA' não encontrada no DataFrame.")
st.markdown("### 🧯 Backlog de OS Abertas")

# 🟡 Filtra OS que ainda estão abertas ou pendentes
df_backlog = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente'])].copy()
total_backlog = len(df_backlog)

# Card visual
st.markdown(f"""
<div style="background-color:#fff3cd; padding:1rem; border-radius:10px; border-left:6px solid #ffc107; margin-bottom:1rem;">
    <div style="font-size:0.95rem; color:#856404;">🔄 Total atual de OS em Backlog</div>
    <div style="font-size:2rem; font-weight:bold; color:#856404;">{total_backlog}</div>
</div>
""", unsafe_allow_html=True)

# 🔄 Evolução do backlog mês a mês
df_filtrado['Mes_Ano'] = df_filtrado['Abertura'].dt.to_period('M').astype(str)
df_backlog_mensal = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente'])].copy()

# Conta acumulado mês a mês
evolucao_backlog = df_backlog_mensal.groupby('Mes_Ano')['OS'].count().reset_index(name='Backlog')
evolucao_backlog['Mes_Ano_Data'] = pd.to_datetime(evolucao_backlog['Mes_Ano'], format='%Y-%m')
evolucao_backlog = evolucao_backlog.sort_values('Mes_Ano_Data')

import plotly.graph_objects as go

# Gráfico com tendência de backlog (subida = vermelho, queda = verde)
fig_backlog = go.Figure()

x = evolucao_backlog['Mes_Ano'].tolist()
y = evolucao_backlog['Backlog'].tolist()

for i in range(len(x) - 1):
    cor = "#dc3545" if y[i+1] > y[i] else "#28a745"  # vermelho se subiu, verde se caiu
    fig_backlog.add_trace(go.Scatter(
        x=[x[i], x[i+1]],
        y=[y[i], y[i+1]],
        mode='lines+markers+text',
        line=dict(color=cor, width=3),
        marker=dict(size=8),
        text=[f"{y[i]}", f"{y[i+1]}"],
        textposition="top center",
        showlegend=False
    ))

fig_backlog.update_layout(
    height=420,
    title="Evolução do Backlog de OS Abertas com Indicador de Tendência",
    xaxis_title="Mês de Abertura",
    yaxis_title="Qtde de OS Abertas",
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=50, b=60)
)

st.plotly_chart(fig_backlog, use_container_width=True)

# 🔽 Exportar somente OS em Backlog com colunas de 'OS' até 'Nº Chamado'
df_backlog_export = df_filtrado[df_filtrado['SITUAÇÃO OS'].isin(['Aberta', 'Pendente'])].copy()

# Seleciona da coluna 'OS' até 'Nº Chamado'
if 'OS' in df_backlog_export.columns and 'Nº Chamado' in df_backlog_export.columns:
    colunas_exportar = df_backlog_export.loc[:, 'OS':'Nº Chamado']
else:
    st.warning("❗ Colunas 'OS' e 'Nº Chamado' não foram localizadas corretamente.")
    colunas_exportar = df_backlog_export.copy()

# Exporta para XLSX
from io import BytesIO
import xlsxwriter

output_backlog = BytesIO()
with pd.ExcelWriter(output_backlog, engine='xlsxwriter') as writer:
    colunas_exportar.to_excel(writer, index=False, sheet_name='Backlog')
dados_xlsx_backlog = output_backlog.getvalue()

st.download_button(
    label="📥 Baixar OS em Backlog (Excel)",
    data=dados_xlsx_backlog,
    file_name="backlog_detalhado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("### 🛠️ Quantidade de OS Pendentes por Tipo de Pendência")

# Verifica se as colunas necessárias existem
if 'SITUAÇÃO OS' in df_filtrado.columns and 'Tipo de Pendência' in df_filtrado.columns:

    # Filtra OS com situação "Pendente"
    df_pendencias = df_filtrado[df_filtrado['SITUAÇÃO OS'] == 'Pendente'].copy()

    # Agrupa por Tipo de Pendência e conta o número de OS
    pendencias_tipo = df_pendencias['Tipo de Pendência'].value_counts().reset_index()
    pendencias_tipo.columns = ['Tipo de Pendência', 'Qtd de OS']

    # Ordena
    pendencias_tipo = pendencias_tipo.sort_values(by='Qtd de OS', ascending=True)

    # Cria gráfico horizontal com Plotly
    import plotly.express as px

    fig_pendencias = px.bar(
        pendencias_tipo,
        x='Qtd de OS',
        y='Tipo de Pendência',
        orientation='h',
        color='Qtd de OS',
        color_continuous_scale='Sunset',
        text='Qtd de OS'
    )

    fig_pendencias.update_layout(
        xaxis_title="Quantidade de OS",
        yaxis_title="Tipo de Pendência",
        title="OS Pendentes por Tipo de Pendência",
        height=500,
        coloraxis_showscale=False
    )

    fig_pendencias.update_traces(textposition='outside')

    st.plotly_chart(fig_pendencias, use_container_width=True)

else:
    st.warning("⚠️ Coluna 'Tipo de Pendência' não encontrada no DataFrame.")


