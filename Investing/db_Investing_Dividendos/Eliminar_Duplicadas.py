import mysql.connector

class EliminacaoDeDuplicatas:
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

    def eliminar_duplicatas(self):
        try:
            # Conectar ao banco de dados
            self.conectar_banco_de_dados()

            # Consulta SQL para eliminar duplicatas mantendo a entrada com o menor id para cada simbolo
            consulta_eliminar_duplicatas = f"""
                DELETE t1 FROM {self.tabela} t1
                JOIN {self.tabela} t2 ON t1.simbolo = t2.simbolo AND t1.id > t2.id
            """

            # Executar a consulta SQL
            self.cursor.execute(consulta_eliminar_duplicatas)

            # Commit e fechar o cursor
            self.conexao.commit()

            print("Linhas duplicadas eliminadas com sucesso.")

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            # Desconectar do banco de dados
            self.fechar_conexao()

# Exemplo de uso
eliminador = EliminacaoDeDuplicatas("localhost", "developer", "Leo140707", "RaspagemPuraDeDados", "index_de_acoes")
eliminador.eliminar_duplicatas()
