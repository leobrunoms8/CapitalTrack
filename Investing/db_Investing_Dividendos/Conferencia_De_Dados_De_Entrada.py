from Coleta_Simbolo_Na_Tabela_De_Raspagem import Coleta_Simbolo_Na_Tabela_De_Raspagem
from Coleta_Empresa_Na_Tabela_De_Raspagem import Coleta_Empresa_Na_Tabela_De_Raspagem
from Analise_Simbolos_Yfinance import Analise_De_Simbolos


# Instacia classe para coleta de simbolos
coletor = Coleta_Simbolo_Na_Tabela_De_Raspagem(
    host="localhost",
    usuario="developer",
    senha="Leo140707",
    banco_de_dados="RaspagemPuraDeDados",
    tabela="raspagem"
)

lista_simbolos = coletor.obter_lista_de_simbolos()

# Imprimir a lista no terminal
print("Lista de Símbolos:")
for simbolo in lista_simbolos:
    print(simbolo, " do tipo: ", type(simbolo))

# Instacia classe para coleta dos nomes das empresas
coletor = Coleta_Empresa_Na_Tabela_De_Raspagem(
    host="localhost",
    usuario="developer",
    senha="Leo140707",
    banco_de_dados="RaspagemPuraDeDados",
    tabela="raspagem"
)

lista_empresa = coletor.obter_lista_de_empresa()

# Imprimir a lista no terminal
print("Lista de Símbolos:")
for empresa in lista_empresa:
    print(empresa)

# Cria uma instância da classe
analise_simbolos = Analise_De_Simbolos(lista_simbolos)

# Executa a verificação dos símbolos
analise_simbolos.verificar_simbolos()

# Obtém os resultados
resultados = analise_simbolos.obter_resultados()

# Imprime os símbolos encontrados e não encontrados
print("Símbolos Encontrados:")
print(resultados['simbolos_encontrados'])

print("\nSímbolos Não Encontrados:")
print(resultados['simbolos_nao_encontrados'])