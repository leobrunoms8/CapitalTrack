import mysql.connector

class ApagarTabela:
    def __init__(self,host, user, password, database):
        self
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def apagar_tabela(self):
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            # Criar um cursor para executar consultas SQL
            cursor = db.cursor()

            # Substitua "sua_tabela" pelo nome da tabela que você deseja apagar
            tabela_a_apagar = 'raspagem'

            # Comando SQL para apagar a tabela
            query = f"DROP TABLE {tabela_a_apagar}"

            # Executar o comando SQL
            cursor.execute(query)

            # Commit para salvar as alterações no banco de dados
            db.commit()

        except Exception as err:
            print(err)
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()
