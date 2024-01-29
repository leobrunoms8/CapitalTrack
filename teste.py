def obter_tabelas(self):
        tabelas = []
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )
            cursor = self.conexao.cursor()
            cursor.execute("SHOW TABLES")
            for tabela in cursor.fetchall():
                tabelas.append(tabela[0])
            return tabelas
        except mysql.connector.Error as erro:
            print("Erro ao obter tabelas:", erro)
            return None
