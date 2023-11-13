import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        # Criar a tabela
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_data(self, table_name, data):
        # Inserir dados na tabela
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(data[0]))})"
        self.cursor.executemany(insert_query, data)
        self.connection.commit()

    def close_connection(self):
        # Fechar a conexão com o banco de dados
        self.connection.close()


class Main:
    def __init__(self):
        self.db = MySQLDatabase(
            host='seu_host',
            user='seu_usuario',
            password='sua_senha',
            database='seu_banco_de_dados'
        )

    def create_table_from_list(self, table_name, columns, data):
        # Criar a tabela no banco de dados
        self.db.create_table(table_name, columns)

        # Inserir dados na tabela
        self.db.insert_data(table_name, data)

    def run_example(self):
        table_name = 'exemplo_tabela'
        columns = ['id INT AUTO_INCREMENT PRIMARY KEY', 'nome VARCHAR(255)', 'idade INT']
        data = [
            (1, 'João', 25),
            (2, 'Maria', 30),
            (3, 'Pedro', 22)
        ]

        # Criar a tabela e inserir dados
        self.create_table_from_list(table_name, columns, data)

        # Fechar a conexão com o banco de dados
        self.db.close_connection()


if __name__ == "__main__":
    main = Main()
    main.run_example()
