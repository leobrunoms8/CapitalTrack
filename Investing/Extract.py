from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import openpyxl
import time

# Fazer uma solicitação HTTP para a página
url = "https://br.investing.com/dividends-calendar/"  # Substitua pela URL real
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

# Criar um arquivo Excel e adicionar os dados a uma planilha
workbook = openpyxl.Workbook()
sheet = workbook.active
for linha in dados:
    sheet.append(linha)

# Salvar o arquivo Excel
workbook.save("dados_Rev2.xlsx")
