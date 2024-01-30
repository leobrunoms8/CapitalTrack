import mysql.connector

class Formatar_Tabelas:
    def __init__(self):
        self.conexao = None

    def adicionar_coluna(self, tabela, nome_da_coluna, tipo):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )
            cursor = self.conexao.cursor()
            query = f"ALTER TABLE `{tabela}` ADD COLUMN `{nome_da_coluna}` {tipo}"
            cursor.execute(query)
            self.conexao.commit()
            print(f"Coluna '{nome_da_coluna}' adicionada com sucesso à tabela '{tabela}'.")
        except mysql.connector.Error as erro:
            print("Erro ao adicionar coluna:", erro)
        finally:
            if self.conexao:
                self.conexao.close()
