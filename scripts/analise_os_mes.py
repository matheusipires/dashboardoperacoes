# scripts/analise_os_mes.py

def calcular_os_por_mes(df):
    """Agrupa os dados e calcula quantidade de OS por mês."""
    df['Mes_Ano'] = df['Abertura'].dt.to_period('M').astype(str)
    resumo = df.groupby('Mes_Ano')['OS'].count().reset_index()
    resumo.columns = ['Mês', 'Quantidade_OS']
    return resumo
