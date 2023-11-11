from Investing.extract_Dados import InvestingScraper
from db.Info_Data import InfoList
from db.Array_dados import DadosParser

# Criar uma instância da classe InvestingScraper
investing_scraper = InvestingScraper("https://br.investing.com/dividends-calendar/")

# Chamar o método scrape_data para obter a lista de dados
dados = investing_scraper.scrape_data()

# Manipular os dados conforme necessário
for linha in dados:
    print("\t".join(linha))

# Tratar Lista

infoList = InfoList(dados)
infoList.print_info()


# Criar uma instância da classe
parser = DadosParser(dados)

# Processar os dados
parser.processar_dados()

# Obter os resultados
resultados = parser.obter_resultados()

# Imprimir os resultados
for i, resultado in enumerate(resultados, start=1):
    print(f"Resultados da Linha {i}: {resultado}")
