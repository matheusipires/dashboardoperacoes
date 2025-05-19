# main.py

from scripts.leitura_dados import carregar_dados
from scripts.analise_os_mes import calcular_os_por_mes
import matplotlib.pyplot as plt

# Carrega e trata os dados
df = carregar_dados()

# Calcula OS por mês
resumo = calcular_os_por_mes(df)

# Mostra o gráfico
plt.figure(figsize=(10, 5))
plt.plot(resumo['Mês'], resumo['Quantidade_OS'], marker='o')
plt.xticks(rotation=45)
plt.title('Quantidade de OS por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de OS')
plt.grid(True)
plt.tight_layout()
plt.show()