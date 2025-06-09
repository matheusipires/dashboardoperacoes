import pandas as pd
import gdown
import os

def carregar_dados():
    file_id = "1nwiU-O9DNjWGJ2C5PMp65uG2YBVoZnxM"
    output = "/tmp/dados.xlsx"

    # Baixa o arquivo do Google Drive
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

    # Verifica se o arquivo foi salvo corretamente
    if not os.path.exists(output):
        raise FileNotFoundError("Erro ao baixar o arquivo Excel.")

    # Lê a planilha local com engine explícito
    df = pd.read_excel(output, sheet_name="Dados sistemas fechadas", engine="openpyxl")

    # Garante que as colunas de datas estão no formato correto
    df['Abertura'] = pd.to_datetime(df['Abertura'], errors='coerce')
    df['Fechamento'] = pd.to_datetime(df['Fechamento'], errors='coerce')

    return df
