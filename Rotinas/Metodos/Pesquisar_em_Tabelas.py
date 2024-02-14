import mysql.connector

class PesquisarEmTabelas:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def nome_da_empresa_com_simbolo(self, simbolo):
        # Conecte ao banco de dados MySQL
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        tabelas = []
        
        try:
            # Criar um cursor para executar consultas SQL
            cursor = db.cursor()

            # Consultar as tabelas no banco de dados
            cursor.execute("SHOW TABLES")

            # Obter resultados da consulta
            tabelas = cursor.fetchall()
 
            for tabela in tabelas:
                print(tabela)
                nova_tabela = tabela[0]
                print(nova_tabela)
                
                try:
                    # Criar um cursor para executar consultas SQL
                    cursor = db.cursor()

                    # Execute uma consulta para obter dados da tabela correspondente ao símbolo escolhido
                    consulta_sql = f"SELECT nome_da_empresa FROM `{nova_tabela}` WHERE simbolo = %s"
                    cursor.execute(consulta_sql, (simbolo,))

                    resultados_dos_valores = cursor.fetchone()
                    print(resultados_dos_valores)
                    if resultados_dos_valores == None:

                        continue
                    nome_da_empresa = resultados_dos_valores[0]
                    return nome_da_empresa

                except mysql.connector.Error as e:
                    print(f"Erro ao consultar Nome da Empresa de: {simbolo}: {e}")
                    continue
            
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()

    def moeda_com_simbolo(self, simbolo):
        # Conecte ao banco de dados MySQL
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        tabelas = []
        
        try:
            # Criar um cursor para executar consultas SQL
            cursor = db.cursor()

            # Consultar as tabelas no banco de dados
            cursor.execute("SHOW TABLES")

            # Obter resultados da consulta
            tabelas = cursor.fetchall()
 
            for tabela in tabelas:
                print(tabela)
                nova_tabela = tabela[0]
                print(nova_tabela)
                
                try:
                    # Criar um cursor para executar consultas SQL
                    cursor = db.cursor()

                    # Execute uma consulta para obter dados da tabela correspondente ao símbolo escolhido
                    consulta_sql = f"SELECT moeda FROM `{nova_tabela}` WHERE simbolo = %s"
                    cursor.execute(consulta_sql, (simbolo,))

                    resultados_dos_valores = cursor.fetchone()
                    print(resultados_dos_valores)
                    if resultados_dos_valores == None:

                        continue
                    moeda = resultados_dos_valores[0]
                    return moeda

                except mysql.connector.Error as e:
                    print(f"Erro ao consultar Nome da Empresa de: {simbolo}: {e}")
                    continue
            
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()
   
