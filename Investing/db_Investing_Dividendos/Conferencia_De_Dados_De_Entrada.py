from Coleta_Simbolo_Na_Tabela_De_Raspagem import Coleta_Simbolo_Na_Tabela_De_Raspagem
from Coleta_Empresa_Na_Tabela_De_Raspagem import Coleta_Empresa_Na_Tabela_De_Raspagem
from Correção_de_Banco_de_Dados import Correcao_de_banco_de_dados
from Gerenciador_Tabela_De_Acoes import GerenciadorTabelaAcoes
from Analise_Simbolos_Yfinance import Analise_De_Simbolos

#info conexão
info_conexao_raspagem = ["localhost", "developer", "Leo140707", "RaspagemPuraDeDados", "raspagem"]

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

# Cria uma instância da classe
analise_simbolos = Analise_De_Simbolos(lista_simbolos)

# Executa a verificação dos símbolos
analise_simbolos.verificar_simbolos()

# Obtém os resultados
encontrados = analise_simbolos.obter_resultados()


# Imprime os símbolos encontrados e não encontrados
print("Símbolos Encontrados:")
print(encontrados)

# Coleta o nome da Empresa de acordo com os simbolos encontrados
consulta = Coleta_Empresa_Na_Tabela_De_Raspagem(
    host="localhost",
    usuario="developer",
    senha="Leo140707",
    banco_de_dados="RaspagemPuraDeDados",
    tabela="raspagem"
    )
empresas = consulta.executar_consulta(encontrados)

# Imprimir Lista Simbolos/Empresas no terminal
print(empresas)


gerenciador_acoes = GerenciadorTabelaAcoes(
    host="localhost",
    usuario="developer",
    senha="Leo140707",
    banco_de_dados="RaspagemPuraDeDados",
    tabela="raspagem"
)
gerenciador_acoes.criar_tabela()

# Inserir empresas em lista de empresas conferidas pelo Yfinance
gerenciador_acoes.inserir_linha(empresas)

# Correção de erro no banco de dadosd e ações
correcao = Correcao_de_banco_de_dados("localhost", "developer", "Leo140707", "RaspagemPuraDeDados", "index_de_acoes")
correcao.correcao_de_banco_de_dados()