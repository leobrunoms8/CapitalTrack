import mysql.connector
from datetime import datetime

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
                    print(f"Erro ao consultar Moeda de: {simbolo}: {e}")
                    continue
            
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()
   
    def frequencia_com_simbolo(self, simbolo):
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
                    consulta_sql = f"SELECT frequencia FROM `{nova_tabela}` WHERE simbolo = %s"
                    cursor.execute(consulta_sql, (simbolo,))

                    resultados_dos_valores = cursor.fetchone()
                    print(resultados_dos_valores)
                    if resultados_dos_valores == None:

                        continue
                    moeda = resultados_dos_valores[0]
                    return moeda

                except mysql.connector.Error as e:
                    print(f"Erro ao consultar Frequencia de: {simbolo}: {e}")
                    continue
            
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()
    
    def proximo_dividendo_com_simbolo(self, simbolo):
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
                    consulta_sql = f"SELECT data_ex FROM `{nova_tabela}` WHERE simbolo = %s"
                    cursor.execute(consulta_sql, (simbolo,))

                    resultados_dos_valores = cursor.fetchone()
                    print(resultados_dos_valores)
                    if resultados_dos_valores == None:

                        continue
                    data_ex = resultados_dos_valores[0]

                    #Data atual
                    data_atual = datetime.now()

                    # Converter a string em um objeto de data
                    data_ex_date = datetime.strptime(data_ex, '%d.%m.%Y')

                    # Comparar a data_ex com a data atual
                    if data_ex_date > data_atual:
                        return data_ex
                    else:
                        return None
                    
                except mysql.connector.Error as e:
                    print(f"Erro ao consultar Nome da Empresa de: {simbolo}: {e}")
                    continue
            
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()
    
    def valor_dividendo_com_simbolo(self, simbolo):
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
                    consulta_sql = f"SELECT valor_dividendo FROM `{nova_tabela}` WHERE simbolo = %s"
                    cursor.execute(consulta_sql, (simbolo,))

                    resultados_dos_valores = cursor.fetchone()
                    print(resultados_dos_valores)
                    if resultados_dos_valores == None:

                        continue
                    valor_do_dividendo = resultados_dos_valores[0]
                    return valor_do_dividendo

                except mysql.connector.Error as e:
                    print(f"Erro ao consultar Valor do Dividendo de: {simbolo}: {e}")
                    continue
            
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            db.close()
    
    def trade_com_id(self, id):
        # Conecte ao banco de dados MySQL
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        try:
            # Criar um cursor para executar consultas SQL
            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente ao símbolo escolhido
            consulta_sql = f"SELECT valor_de_entrada, quantidade_de_entrada FROM lista_de_trades WHERE id = %s"
            cursor.execute(consulta_sql, (id,))

            resultados_dos_valores = cursor.fetchone()
            return resultados_dos_valores

        except mysql.connector.Error as e:
                print(f"Erro ao consultar Trade {id}: {e}")
        

   
