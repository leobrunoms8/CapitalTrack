import mysql.connector

def criar_tabela():
    conexao = None
    try:
        # Estabelece a conexão com o servidor MySQL e seleciona o banco de dados "Stocks"
        conexao = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="Leo140707",
            database="RaspagemPuraDeDados"
        )

        # Cria um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Comando SQL para criar a tabela com as colunas desejadas
        criar_tabela_sql = """
        CREATE TABLE IF NOT EXISTS lista_de_trades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            simbolo VARCHAR(255),
            valor_de_entrada FLOAT,
            quantidade_de_entrada DECIMAL(10, 2),
            data_de_entrada DATE,
            valor_dividendo FLOAT,
            valor_premio FLOAT,
            data_ex DATE,
            data_pagamento DATE,
            coretora VARCHAR(50),
            moeda VARCHAR(50),
            valor_de_saida FLOAT,
            quantidade_de_saida DECIMAL(10, 2),
            data_de_saida DATE,
            ganho_real FLOAT,
            ganho_percentual FLOAT,
            acerto VARCHAR(255),
            link_para_trade INT
        )
        """
        cursor.execute(criar_tabela_sql)

        print("Tabela 'lista_de_trades' criada com sucesso.")

    except mysql.connector.Error as erro:
        print(f"Erro ao criar a tabela: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

# Chame a função para criar a tabela
criar_tabela()
