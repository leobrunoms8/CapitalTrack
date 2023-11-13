from Investing.extract_Dados import InvestingScraper
from db.Info_Data import InfoList
from Investing.db_Investing_Dividendos.Raspagem_Pura_De_Dados import criar_banco_de_dados
from Investing.db_Investing_Dividendos.Criar_Tabela_Raspagem import criar_tabela
from Investing.db_Investing_Dividendos.Inserir_Dados_Raspagem import InsercaoDados

# Criar uma instância da classe InvestingScraper
investing_scraper = InvestingScraper("https://br.investing.com/dividends-calendar/")

# Chamar o método scrape_data para obter a lista de dados
dados = investing_scraper.scrape_data()

# Imprimir dados obtidos no Investing.com no terminal
for linha in dados:
    print("\t".join(linha))

# Tratar Lista
infoList = InfoList(dados)
infoList.print_info()

# Cria um Banco de Dados com o Nome Raspagem de Dados Pura 
# Chame a função para criar o banco de dados
criar_banco_de_dados()

# Chame a função para criar a tabela raspagem
criar_tabela()

# Chame a função para inserir os dados 
insercao = InsercaoDados(dados)
insercao.inserir_dados()
