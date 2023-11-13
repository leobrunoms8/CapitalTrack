import numpy as np

class ProcessadorDeStrings:
    def __init__(self, data):
        self.data = data

    def tabulacao_dados(self):
        # Lista para armazenar as informações extraídas
        informacoes = []

        # Itera sobre cada lista na lista principal
        for lista in self.data:
            # Itera sobre cada string na lista interna
            for linha in lista:
                
                # Adiciona a lista resultante à lista de informações
                informacoes.append(linha)

        # Converte a lista de listas para um array NumPy
        informacoes_np = np.array(informacoes)

        # Retorna o array resultante
        return informacoes_np

# Criar uma instância da classe
processador = ProcessadorDeStrings(
    vazio   AOD     Abrdn Total Dynamic Dividend Fund       21.11.2023      0,0575  vazio   30.11.2023      9,26%
vazio   HQL     Abrdn Life Sciences Investors   21.11.2023      0,3     vazio   10.01.2024      10,11
)

# Chama o método tabulacao_dados
resultado = processador.tabulacao_dados()

# Imprime a matriz indexada no terminal
print("Matriz Indexada:")
print(resultado[3][3])
