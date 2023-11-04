import mysql.connector

def criar_banco_de_dados():
    try:
        # Estabelece a conexão com o servidor MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="Leo140707"
        )

        # Cria um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Comando SQL para criar o banco de dados "Stocks"
        comando_sql = "CREATE DATABASE IF NOT EXISTS Stocks"

        # Executa o comando SQL
        cursor.execute(comando_sql)

        print("Banco de dados 'Stocks' criado com sucesso.")

    except mysql.connector.Error as erro:
        print(f"Erro ao criar o banco de dados: {erro}")

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

# Chame a função para criar o banco de dados
criar_banco_de_dados()
