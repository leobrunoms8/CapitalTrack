from .db_Investing_Dividendos.Coleta_Simbolo_Na_Tabela_De_Raspagem import Coleta_Simbolo_Na_Tabela_De_Raspagem
from .db_Investing_Dividendos.Coleta_Empresa_Na_Tabela_De_Raspagem import Coleta_Empresa_Na_Tabela_De_Raspagem
from .db_Investing_Dividendos.Correção_de_Banco_de_Dados import Correcao_de_banco_de_dados
from .db_Investing_Dividendos.Gerenciador_Tabela_De_Acoes import GerenciadorTabelaAcoes
from .db_Investing_Dividendos.Analise_Simbolos_Yfinance import Analise_De_Simbolos
from .db_Investing_Dividendos.Separar_Por_Data_Ex import SeparadorPorDataEx

class AnaliseSimbolosManager:
    def __init__(self, info_conexao):
        self.info_conexao = info_conexao

    def executar_analise(self):
        # Instancia classe para coleta de simbolos
        coletor = Coleta_Simbolo_Na_Tabela_De_Raspagem(*self.info_conexao)
        lista_simbolos = coletor.obter_lista_de_simbolos()

        # Imprimir a lista no terminal
        print("Lista de Símbolos:")
        for simbolo in lista_simbolos:
            print(simbolo, " do tipo: ", type(simbolo))
        
        # Separar ações em tabelas por Data EX
        # Configurações de conexão ao banco de dados
        db_config = {
            'host': 'localhost',
            'user': 'developer',
            'password': 'Leo140707',
            'database': 'RaspagemPuraDeDados'
        }

        # Criar instância da classe e chamar o método separar_por_data_ex
        separador = SeparadorPorDataEx(db_config)
        separador.separar_por_data_ex()
        separador.fechar_conexao()     

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
        consulta = Coleta_Empresa_Na_Tabela_De_Raspagem(*self.info_conexao)
        empresas = consulta.executar_consulta(encontrados)

        # Imprimir Lista Simbolos/Empresas no terminal
        print(empresas)

        gerenciador_acoes = GerenciadorTabelaAcoes(*self.info_conexao)
        gerenciador_acoes.criar_tabela()

        # Inserir empresas em lista de empresas conferidas pelo Yfinance
        gerenciador_acoes.inserir_linha(empresas)

        # Correção de erro no banco de dados de ações
        correcao = Correcao_de_banco_de_dados(*self.info_conexao)
        correcao.correcao_de_banco_de_dados()


