import mysql.connector




class Atualizar_Tabelas:
    def __init__(self):
        self.conexao = None

    def atualizar_tabela_dividendos_moeda(self, tabela, simbolo, moeda):
        print(tabela)
        print(simbolo)
        print(moeda)

        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )
            cursor = self.conexao.cursor()
            query = f"UPDATE `{tabela}` SET moeda = %s WHERE simbolo = %s"
            cursor.execute(query, (moeda, simbolo))
            self.conexao.commit()
            print("Moeda atualizada com sucesso!")

        except mysql.connector.Error as erro:
            print("Erro ao atualizar moeda:", erro)
        finally:
            cursor.close()
            self.conexao.close()

    def atualizar_tabela_dividendos_frequencia(self, tabela, simbolo, frequencia):
        print(tabela)
        print(simbolo)
        print(frequencia)

        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )
            cursor = self.conexao.cursor()
            query = f"UPDATE `{tabela}` SET frequencia = %s WHERE simbolo = %s"
            cursor.execute(query, (frequencia, simbolo))
            self.conexao.commit()
            print("Frequência atualizada com sucesso!")

        except mysql.connector.Error as erro:
            print("Erro ao atualizar frequência:", erro)
        finally:
            cursor.close()
            self.conexao.close()

    def atualizar_tabela_dividendos_relacao(self, tabela, simbolo, relacao):
        print(tabela)
        print(simbolo)
        print(relacao)

        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )
            cursor = self.conexao.cursor()
            query = f"UPDATE `{tabela}` SET dividendo_acao = %s WHERE simbolo = %s"
            cursor.execute(query, (relacao, simbolo))
            self.conexao.commit()
            print("Relação atualizada com sucesso!")

        except mysql.connector.Error as erro:
            print("Erro ao atualizar Relação:", erro)
        finally:
            cursor.close()
            self.conexao.close()


   
