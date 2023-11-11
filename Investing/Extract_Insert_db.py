from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import re

# Fazer uma solicitação HTTP para a página
url = "https://br.investing.com/dividends-calendar/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Inicializar o driver do Selenium
driver = webdriver.Chrome()  # Certifique-se de ter o ChromeDriver instalado

# Navegar para a página
driver.get(url)

# Localizar o link "Amanhã" usando Selenium
link_amanha = driver.find_element(By.ID, "timeFrame_nextWeek")

# Clicar no link "Amanhã"
link_amanha.click()

# Aguardar 5 segundos para a página ser atualizada
time.sleep(5)

# Obter o HTML da página atualizada
page_source = driver.page_source

# Aguardar um curto período de tempo para que a página seja atualizada (você pode ajustar o tempo conforme necessário)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "dividendsCalendarData")))

# Obter o HTML da página atualizada
page_source = driver.page_source

# Fechar o navegador Selenium
driver.quit()

# Analisar o HTML da página atualizada com BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Localizar a tabela desejada
tabela = soup.find("table", {"id": "dividendsCalendarData"})

# Extrair os dados da tabela e armazená-los em uma lista
dados = []
for linha in tabela.find_all("tr"):
    celulas = linha.find_all("td")
    linha_dados = [c.text.strip() for c in celulas]
    if linha_dados:  # Ignorar linhas vazias
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

# Mostrar os dados no terminal
for linha in dados:
    print("\t".join(linha))
