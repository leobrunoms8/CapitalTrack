import mysql.connector

class CriarTabelaGenerico:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def criar_tabela_generico(self, comando):
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

            cursor.execute(comando)

            print("Tabela 'rascunho' criada com sucesso.")

        except mysql.connector.Error as erro:
            print(f"Erro ao criar a tabela: {erro}")

        finally:
            if db is not None and db.is_connected():
                cursor.close()
                db.close()
                print("Conexão encerrada.") 
    