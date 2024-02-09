import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

class SeparadorPorDataEx:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        self.cursor = self.conn.cursor()
        self.engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

    def separar_por_data_ex(self):
        # Consulta para obter todas as datas únicas da coluna "data_ex"
        query_datas = "SELECT DISTINCT data_ex FROM raspagem"
        self.cursor.execute(query_datas)
        datas = [data[0] for data in self.cursor.fetchall()]

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
            df = pd.read_sql_query(query_dados, self.conn)

            # Criar uma nova tabela com os dados agrupados
            nova_tabela = f"tabela_{data.replace('-', '_')}"
            df.to_sql(nova_tabela, self.engine, index=False, if_exists='replace')

    def fechar_conexao(self):
        # Fechar conexão
        self.conn.close()


