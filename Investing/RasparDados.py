from .db_Investing_Dividendos.extract_Dados import InvestingScraper
from .db_Investing_Dividendos.Info_Data import InfoList
from .db_Investing_Dividendos.Raspagem_Pura_De_Dados import criar_banco_de_dados
from .db_Investing_Dividendos.Criar_Tabela_Raspagem import criar_tabela
from .db_Investing_Dividendos.Inserir_Dados_Raspagem import InsercaoDados
from .db_Investing_Dividendos.Apagar_Tabela_Raspagem import ApagarTabela
from .Conferencia_De_Dados_De_Entrada import AnaliseSimbolosManager

class RaspagemInvesting:
    def __init__(self, url):
        self.investing_scraper = InvestingScraper(url)
        self.dados = None

    def realizar_raspagem(self):
        # Dropar Lista raspagem 
        self.apagar = ApagarTabela()
        self.apagar.apagar_tabela()

        # Chamar o método scrape_data para obter a lista de dados
        self.dados = self.investing_scraper.scrape_data()

        # Imprimir dados obtidos no Investing.com no terminal
        for linha in self.dados:
            print("\t".join(linha))

        # Tratar Lista
        infoList = InfoList(self.dados)
        infoList.print_info()

        # Cria um Banco de Dados com o Nome Raspagem de Dados Pura
        # Criar o banco de dados
        criar_banco_de_dados()

        # Criar a tabela raspagem
        criar_tabela()

        # Chame a função para inserir os dados
        insercao = InsercaoDados(self.dados)
        insercao.inserir_dados()

        # Info conexão
        info_conexao_raspagem = ["localhost", "developer", "Leo140707", "RaspagemPuraDeDados", "raspagem"]

        # Cria uma instância da classe e executa o método
        analise_manager = AnaliseSimbolosManager(info_conexao_raspagem)
        analise_manager.executar_analise()


