import mysql.connector
from .Formatar_Tabelas import Formatar_Tabelas




class Atualizar_Tabelas:
    def __init__(self, host, user, password, database):
        self.conexao = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database


    def atualizar_tabela_dividendos_moeda(self, tabela, simbolo, moeda):
        # Criação da coluna 'Moeda':
        formatador = Formatar_Tabelas()
        formatador.adicionar_coluna(tabela, "moeda", "VARCHAR(255)")

        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = db.cursor()

            query = f"UPDATE {tabela} SET moeda = %s WHERE simbolo = %s"
            cursor.execute(query, (moeda, simbolo))
            db.commit()
            print("Moeda atualizada com sucesso!")

        except mysql.connector.Error as erro:
            print("Erro ao atualizar moeda:", erro)
        finally:
            cursor.close()
            db.close()

    def atualizar_tabela_dividendos_frequencia(self, tabela, simbolo, frequencia):
        # Criação da coluna 'frequencia':
        formatador = Formatar_Tabelas()
        formatador.adicionar_coluna(tabela, "frequencia", "VARCHAR(255)")

        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = db.cursor()
            query = f"UPDATE {tabela} SET frequencia = %s WHERE simbolo = %s"
            cursor.execute(query, (frequencia, simbolo))
            db.commit()
            print("Frequência atualizada com sucesso!")

        except mysql.connector.Error as erro:
            print("Erro ao atualizar frequência:", erro)
        finally:
            cursor.close()
            db.close()

    def atualizar_tabela_dividendos_relacao(self, tabela, simbolo, relacao):
        # Criação da coluna 'Relaão Dividendo por Valor da Ação':
        formatador = Formatar_Tabelas()
        formatador.adicionar_coluna(tabela, "dividendo_acao", "FLOAT")

        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = db.cursor()
            query = f"UPDATE {tabela} SET dividendo_acao = %s WHERE simbolo = %s"
            cursor.execute(query, (relacao, simbolo))
            db.commit()
            print("Relação atualizada com sucesso!")

        except mysql.connector.Error as erro:
            print("Erro ao atualizar Relação:", erro)
        finally:
            cursor.close()
            db.close()

    def atualizar_tabela_trade(self, simbolo, valor_de_entrada, quantidade, data_de_entrada, dividendo, premio, data_ex, data_pagamento, corretora, moeda):
        print(simbolo, valor_de_entrada, quantidade, data_de_entrada, dividendo, premio, data_ex, data_pagamento, corretora, moeda)

        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = db.cursor()

            # Query de inserção de dados
            insert_query = """
            INSERT INTO lista_de_trades (
                simbolo, 
                valor_de_entrada,
                quantidade, 
                data_de_entrada, 
                valor_dividendo, 
                valor_premio, 
                data_ex, 
                data_pagamento, 
                coretora, 
                moeda
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Valores para inserção na tabela
            values = (simbolo, valor_de_entrada, quantidade, data_de_entrada, dividendo, premio, data_ex, data_pagamento, corretora, moeda)

            # Executar a consulta de inserção
            cursor.execute(insert_query, values)

            # Obter o ID da linha inserida
            id_inserido = cursor.lastrowid

            # Commit da transação
            db.commit()

            # Fechar cursor e conexão
            cursor.close()
            db.close()

            # Retorna o ID da linha inserida
            return id_inserido

        except mysql.connector.Error as err:
            print("Erro ao inserir na tabela:", err)
