import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host='localhost',
    user='developer',
    password='Leo140707',
    database='raspagempuradedados'
)

cursor = conexao.cursor()

# Obter nomes das tabelas
cursor.execute("SHOW TABLES;")
tabelas = cursor.fetchall()
print(tabelas)

# Remover caracteres '(', ')', e ',' de cada string
tabelas_formatadas = [tabela[0].replace('(', '').replace(')', '').replace(',', '') for tabela in tabelas]
print(tabelas_formatadas)

# Fechar a conexão
conexao.close()

# Conectar ao banco de dados MySQL
conexao = pymysql.connect(host='localhost', user='developer', password='Leo140707', database='raspagempuradedados')
cursor = conexao.cursor()

# Inicializar lista para armazenar os resultados
dados_resultado = []

# Iterar sobre as tabelas
for tabela in tabelas_formatadas:
    print(tabela)
    # Consulta SQL para obter os dados da tabela
    if tabela == 'index_de_acoes' or tabela == 'raspagem':
        print(tabela)
    else: 
        try:
            consulta_sql = f"SELECT data_ex, SUM(CAST(REPLACE(valor_dividendo, ',', '.') AS DECIMAL(10, 4))) as soma_valor_dividendo FROM `{tabela}` GROUP BY data_ex"
        
            # Executar a consulta SQL
            cursor.execute(consulta_sql)
            
            # Obter os resultados e adicionar à lista
            resultados = cursor.fetchall()
            for resultado in resultados:
                dados_resultado.append({'data': resultado[0], 'soma_valor_dividendo': resultado[1]})

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")
            continue

# Fechar a conexão com o banco de dados fora do loop
conexao.close()

# Criar DataFrame a partir da lista
resultado_df = pd.DataFrame(dados_resultado)

# Substituir '--' por NaN na coluna 'data'
resultado_df['data'] = resultado_df['data'].replace('--', np.nan)

# Converter a coluna 'data' para o tipo datetime, ignorando NaN
resultado_df['data'] = pd.to_datetime(resultado_df['data'], format='%d.%m.%Y', errors='coerce')

# Classificar DataFrame pela coluna 'data'
resultado_df = resultado_df.sort_values(by='data')

# Plotar o gráfico de colunas
plt.bar(resultado_df['data'], resultado_df['soma_valor_dividendo'])
plt.xlabel('Data de Pagamento')
plt.ylabel('Soma do Valor de Dividendo')
plt.title('Soma do Valor de Dividendo por Data de Pagamento')
plt.xticks(rotation=45)
plt.show()