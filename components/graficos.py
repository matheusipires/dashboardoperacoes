import plotly.graph_objects as go
import pandas as pd

def grafico_kpi(grupo_df, cor_azul, cor_verde, cor_laranja):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grupo_df['Mes_Ano_Formatado'],
        y=grupo_df['Total'],
        name='Total de OS Abertas',
        marker_color=cor_azul,
        text=grupo_df['Total'],
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=grupo_df['Mes_Ano_Formatado'],
        y=grupo_df['Fechadas'],
        name='Fechadas no mesmo mês',
        marker_color=cor_verde,
        text=grupo_df['Fechadas'],
        textposition='auto'
    ))
    fig.add_trace(go.Scatter(
        x=grupo_df['Mes_Ano_Formatado'],
        y=grupo_df['% Conclusão'],
        name='% Conclusão',
        mode='lines+markers+text',
        line=dict(color=cor_laranja, dash='dash'),
        text=[f"{x:.1f}%" for x in grupo_df['% Conclusão']],
        textposition="top center",
        yaxis='y2'
    ))

    fig.update_layout(
        xaxis_title='Mês',
        yaxis=dict(title='Quantidade de OS'),
        yaxis2=dict(title='% Conclusão', overlaying='y', side='right', range=[0, 100]),
        barmode='group',
        legend=dict(orientation='h', y=-0.25),
        height=480
    )
    return fig


def grafico_evolucao(grupo_df, cor_azul, cor_laranja):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grupo_df['Mes_Ano_Formatado'],
        y=grupo_df['% Conclusão'],
        mode='lines+markers+text',
        name='% Conclusão',
        text=[f'{v:.1f}%' for v in grupo_df['% Conclusão']],
        textposition='top center',
        line=dict(color=cor_azul)
    ))

    fig.add_trace(go.Scatter(
        x=grupo_df['Mes_Ano_Formatado'],
        y=[90] * len(grupo_df),
        mode='lines',
        name='Meta (90%)',
        line=dict(color=cor_laranja, dash='dash')
    ))

    fig.update_layout(
        title='📈 Evolução Mensal da % Conclusão',
        xaxis_title='Mês',
        yaxis_title='% Conclusão',
        yaxis=dict(range=[0, 100]),
        height=400,
        legend=dict(orientation='h', y=-0.2),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return fig
