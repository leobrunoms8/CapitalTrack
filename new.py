import numpy as np
import matplotlib.pyplot as plt

# Gerando dados para as curvas
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Criando o gráfico e sobrepondo as curvas
plt.plot(x, y1, label='sin(x)')
plt.plot(x, y2, label='cos(x)')

# Adicionando legendas, título e rótulos dos eixos
plt.legend()
plt.title('Curvas Seno e Cosseno')
plt.xlabel('X')
plt.ylabel('Y')

# Exibindo o gráfico
plt.grid(True)
plt.show()
