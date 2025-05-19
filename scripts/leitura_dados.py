import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    url = "https://drive.google.com/uc?export=download&id=1nwiU-O9DNjWGJ2C5PMp65uG2YBVoZnxM"
    
    # Carrega a planilha usando o nome correto da aba
    df = pd.read_excel(url, sheet_name="Dados sistemas fechadas")
    
    # Garante que as colunas de datas estão em datetime
    df['Abertura'] = pd.to_datetime(df['Abertura'], errors='coerce')
    df['Fechamento'] = pd.to_datetime(df['Fechamento'], errors='coerce')
    
    return df