import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Configurações de conexão ao banco de dados
db_config = {
    'host': 'localhost',
    'user': 'developer',
    'password': 'Leo140707',
    'database': 'RaspagemPuraDeDados'
}

# Conectar ao banco de dados
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Consulta para obter todas as datas únicas da coluna "data_ex"
query_datas = "SELECT DISTINCT data_ex FROM raspagem"
cursor.execute(query_datas)
datas = [data[0] for data in cursor.fetchall()]

# Criar engine do SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# Para cada data, criar uma tabela e inserir dados nela
for data in datas:
    # Consulta para obter os dados correspondentes à data atual
    query_dados = f"""
        SELECT
            id,
            simbolo,
            nome_da_empresa,
            data_ex,
            valor_dividendo,
            data_pagamento
        FROM
            raspagem
        WHERE
            data_ex = '{data}'
    """
    
    # Ler os dados do MySQL para um DataFrame pandas
    df = pd.read_sql_query(query_dados, conn)
    
    # Criar uma nova tabela com os dados agrupados
    nova_tabela = f"tabela_{data.replace('-', '_')}"
    df.to_sql(nova_tabela, engine, index=False, if_exists='replace')

# Fechar conexão
conn.close()
