from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import re

class InvestingScraper:
    def __init__(self, periodo):
        self.url = "https://br.investing.com/dividends-calendar/"
        self.driver = webdriver.Chrome()  # Certifique-se de ter o ChromeDriver instalado
        self.periodo = periodo

    def scrape_data(self):
        # Fazer uma solicitação HTTP para a página
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Navegar para a página
        self.driver.get(self.url)

        # Localizar o link recebido usando Selenium
        link_amanha = self.driver.find_element(By.ID, self.periodo)

        # Clicar no link "Amanhã"
        link_amanha.click()

        # Aguardar 5 segundos para a página ser atualizada
        time.sleep(5)

        # Realizar a rolagem para o final da página
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)  # Isso simula a pressão da tecla "End"

        # Aguardar 5 segundos para a página ser atualizada
        time.sleep(5)

        # Aguardar um curto período de tempo para que a página seja atualizada (você pode ajustar o tempo conforme necessário)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "dividendsCalendarData")))

        # Obter o HTML da página atualizada
        page_source = self.driver.page_source

        # Fechar o navegador Selenium
        self.driver.quit()

        # Analisar o HTML da página atualizada com BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Localizar a tabela desejada
        tabela = soup.find("table", {"id": "dividendsCalendarData"})

        # Extrair os dados da tabela e armazená-los em uma lista
        dados = []
        for linha in tabela.find_all("tr"):
            celulas = linha.find_all("td")
            linha_dados = [c.text.strip() if c.text.strip() else "vazio" for c in celulas]
            dados.append(linha_dados)

        # Modificar os dados para adicionar informações entre parênteses em outra célula
        for linha in dados:
            if len(linha) >= 2:
                # Use expressões regulares para encontrar o texto entre parênteses
                informacao_entre_parenteses = re.search(r'\((.*?)\)', linha[1])
                if informacao_entre_parenteses:
                    # Coloque as informações entre parênteses na célula B
                    linha.insert(1, informacao_entre_parenteses.group(1))
                    # Remova as informações entre parênteses da célula original
                    linha[2] = re.sub(r'\(.*?\)', '', linha[2]).strip()

        return dados
