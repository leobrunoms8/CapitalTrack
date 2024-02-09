import mysql.connector

class Criar_Tabela:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def criar_tabela(self):
        conexao = None
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            # Cria um cursor para executar comandos SQL
            cursor = db.cursor()

            # Comando SQL para criar a tabela com as colunas desejadas
            criar_tabela_sql = """
            CREATE TABLE IF NOT EXISTS Raspagem (
                id INT AUTO_INCREMENT PRIMARY KEY,
                campo VARCHAR(255) NOT NULL,
                simbolo VARCHAR(255) NOT NULL,
                nome_da_empresa VARCHAR(255) NOT NULL,
                data_ex VARCHAR(255) NOT NULL,
                valor_dividendo VARCHAR(255) NOT NULL,
                frequencia VARCHAR(255) NOT NULL,
                data_pagamento VARCHAR(255) NOT NULL,
                percentual_acao VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(criar_tabela_sql)

            print("Tabela 'Dividendos' criada com sucesso.")

        except mysql.connector.Error as erro:
            print(f"Erro ao criar a tabela: {erro}")

        finally:
            if db is not None and db.is_connected():
                cursor.close()
                db.close()
                print("Conexão encerrada.")


