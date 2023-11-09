import mysql.connector

def criar_tabela():
    conexao = None
    try:
        # Estabelece a conexão com o servidor MySQL e seleciona o banco de dados "Stocks"
        conexao = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="Leo140707",
            database="Stocks"
        )

        # Cria um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Comando SQL para criar a tabela com as colunas desejadas
        criar_tabela_sql = """
        CREATE TABLE IF NOT EXISTS Dividendos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            simbolo VARCHAR(255) NOT NULL,
            nome_da_empresa VARCHAR(255) NOT NULL,
            data_ex DATE NOT NULL,
            valor_dividendo DECIMAL(10, 2) NOT NULL,
            frequencia VARCHAR(50) NOT NULL,
            data_pagamento DATE NOT NULL,
            percentual_acao DECIMAL(5, 2) NOT NULL
        )
        """
        cursor.execute(criar_tabela_sql)

        print("Tabela 'Dividendos' criada com sucesso.")

    except mysql.connector.Error as erro:
        print(f"Erro ao criar a tabela: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

# Chame a função para criar a tabela
criar_tabela()
