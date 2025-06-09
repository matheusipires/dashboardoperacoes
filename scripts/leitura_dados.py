import pandas as pd
import gdown
import streamlit as st

@st.cache_data
def carregar_dados():
    # ID e caminho temporário
    file_id = "1nwiU-O9DNjWGJ2C5PMp65uG2YBVoZnxM"
    output = "/tmp/dados.xlsx"

    # Download do arquivo
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

    # Leitura do Excel
    df = pd.read_excel(output, sheet_name="Dados sistemas fechadas", engine="openpyxl")

    # Conversão de datas
    df['Abertura'] = pd.to_datetime(df['Abertura'], errors='coerce')
    df['Fechamento'] = pd.to_datetime(df['Fechamento'], errors='coerce')

    return df
