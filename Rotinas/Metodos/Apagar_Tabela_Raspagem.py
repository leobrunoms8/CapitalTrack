import mysql.connector

class ApagarTabela:
    def __init__(self):
       self

    def apagar_tabela(self):
        try:  # Estabelece a conexão com o servidor MySQL e seleciona o banco de dados "Stocks"
            conn = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            # Criar um cursor para executar consultas SQL
            cursor = conn.cursor()

            # Substitua "sua_tabela" pelo nome da tabela que você deseja apagar
            tabela_a_apagar = 'raspagem'

            # Comando SQL para apagar a tabela
            query = f"DROP TABLE {tabela_a_apagar}"

            # Executar o comando SQL
            cursor.execute(query)

            # Commit para salvar as alterações no banco de dados
            conn.commit()

        except Exception as err:
            print(err)
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            conn.close()
