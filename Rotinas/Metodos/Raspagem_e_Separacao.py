from .Extrair_Dados_Investing import InvestingScraper
from .Criar_Tabela_Raspagem import Criar_Tabela
from .Inserir_Dados_Raspagem import InsercaoDados
from .Apagar_Tabela_Raspagem import ApagarTabela
from .Separar_Por_Data_Ex import SeparadorPorDataEx

class Raspagem_e_Separacao_Investing:
    def __init__(self, periodo):
        url = "https://br.investing.com/dividends-calendar/"
        self.investing_scraper = InvestingScraper(periodo)
        self.periodo = periodo
        self.dados = None

    def realizar_raspagem(self):
        # Dropar Lista raspagem 
        self.apagar = ApagarTabela()
        self.apagar.apagar_tabela()

        # Criar a tabela raspagem
        self.criar =Criar_Tabela()
        self.criar.criar_tabela()

        # Chamar o método scrape_data para obter a lista de dados
        self.dados = self.investing_scraper.scrape_data()

        # Imprimir dados obtidos no Investing.com no terminal
        for linha in self.dados:
            print("\t".join(linha))
       

        # Chame a função para inserir os dados
        insercao = InsercaoDados(self.dados)
        insercao.inserir_dados()

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



