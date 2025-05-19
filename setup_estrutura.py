import os

# Estrutura de pastas e arquivos
estrutura = {
    "config": ["paths.py"],
    "scripts": ["__init__.py", "leitura_dados.py", "analise_os_mes.py"],
    "app": ["app.py"],
    "outputs": [],
    ".": ["main.py", "requirements.txt"]
}

# Criação das pastas e arquivos
for pasta, arquivos in estrutura.items():
    if pasta != ".":
        os.makedirs(pasta, exist_ok=True)
        print(f"📁 Pasta criada: {pasta}")
    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo) if pasta != "." else arquivo
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("")  # Arquivo vazio
        print(f"📄 Arquivo criado: {caminho}")

print("\n✅ Estrutura criada com sucesso!")
