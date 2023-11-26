import mysql.connector

class Correcao_de_banco_de_dados:
    def __init__(self, host, usuario, senha, banco_de_dados, tabela):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco_de_dados = banco_de_dados
        self.tabela = tabela

    def conectar_banco_de_dados(self):
        # Conectar ao banco de dados
        self.conexao = mysql.connector.connect(
            host=self.host,
            user=self.usuario,
            password=self.senha,
            database=self.banco_de_dados
        )
        self.cursor = self.conexao.cursor()

    def fechar_conexao(self):
        # Fechar a conexão com o banco de dados
            self.cursor.close()
            self.conexao.close()

    def correcao_de_banco_de_dados(self):
        try:
            # Conectar ao banco de dados
            self.conectar_banco_de_dados()

            # Definir a consulta SQL para selecionar a coluna 'simbolo'
            consulta_sql = f"SELECT simbolo FROM {self.tabela}"

            # Executar a consulta SQL
            self.cursor.execute(consulta_sql)

            # Iterar sobre as linhas e inverter as informações se o nome_da_empresa estiver em maiúsculo
            for (simbolo,) in self.cursor:
                # Consulta SQL para obter informações da linha que corresponde ao simbolo
                consulta_update = f"SELECT nome_da_empresa, simbolo FROM {self.tabela} WHERE simbolo = '{simbolo}'"

                # Executar a consulta SQL
                self.cursor.execute(consulta_update)

                # Obter o resultado da consulta
                resultado = self.cursor.fetchall()

                # Se houver resultado, obter as informações
                if resultado:
                    nome_da_empresa_atual, _ = resultado[0]

                    # Atualizar a linha no banco de dados
                    if nome_da_empresa_atual.isupper():
                        atualizar_query = f"UPDATE {self.tabela} SET nome_da_empresa = %s WHERE simbolo = %s"
                        valores = (simbolo, nome_da_empresa_atual)
                        self.cursor.execute(atualizar_query, valores)

            # Commit e fechar o cursor
            self.conexao.commit()

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            # Desconectar do banco de dados
            self.fechar_conexao()


