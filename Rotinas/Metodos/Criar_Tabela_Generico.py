import mysql.connector

class CriarTabelaGenerico:
    def __init__(self):
       self

    def criar_tabela_generico(self, comando):
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

            cursor.execute(comando)

            print("Tabela 'rascunho' criada com sucesso.")

        except mysql.connector.Error as erro:
            print(f"Erro ao criar a tabela: {erro}")

        finally:
            if conexao is not None and conexao.is_connected():
                cursor.close()
                conexao.close()
                print("Conexão encerrada.") 
    