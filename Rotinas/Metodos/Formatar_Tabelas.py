import mysql.connector

class Formatar_Tabelas:
    def __init__(self):
        self.conexao = None

    def verificar_coluna_existente(self, tabela, nome_da_coluna):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )
            cursor = self.conexao.cursor()
            query = f"SHOW COLUMNS FROM {tabela} LIKE %s"
            cursor.execute(query, (nome_da_coluna,))
            resultado = cursor.fetchone()
            if resultado:
                print(f"A coluna '{nome_da_coluna}' já existe na tabela '{tabela}'.")
                return True
            else:
                print(f"A coluna '{nome_da_coluna}' não existe na tabela '{tabela}'.")
                return False
        except mysql.connector.Error as erro:
            print("Erro ao verificar coluna:", erro)
            return False
        finally:
            if self.conexao:
                self.conexao.close()

    def adicionar_coluna(self, tabela, nome_da_coluna, tipo):
        if not self.verificar_coluna_existente(tabela, nome_da_coluna):
            try:
                self.conexao = mysql.connector.connect(
                    host="localhost",
                    user="developer",
                    password="Leo140707",
                    database="RaspagemPuraDeDados"
                )
                cursor = self.conexao.cursor()
                query = f"ALTER TABLE {tabela} ADD COLUMN {nome_da_coluna} {tipo}"
                cursor.execute(query)
                self.conexao.commit()
                print(f"Coluna '{nome_da_coluna}' adicionada com sucesso à tabela '{tabela}'.")
            except mysql.connector.Error as erro:
                print("Erro ao adicionar coluna:", erro)
            finally:
                if self.conexao:
                    self.conexao.close()


