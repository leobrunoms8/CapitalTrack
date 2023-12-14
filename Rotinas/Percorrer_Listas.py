import mysql.connector

class Coleta_Simbolo_Na_Tabela_De_Raspagem:
    def __init__(self, host, usuario, senha, banco_de_dados, tabela, coluna):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco_de_dados = banco_de_dados
        self.tabela = tabela
        self.coluna = coluna

    def conectar_banco_de_dados(self):
        # Conectar ao banco de dados
        self.conexao = mysql.connector.connect(
            host=self.host,
            user=self.usuario,
            password=self.senha,
            database=self.banco_de_dados
        )
        self.cursor = self.conexao.cursor()

    def desconectar_banco_de_dados(self):
        # Fechar o cursor e a conexão com o banco de dados
        self.cursor.close()
        self.conexao.close()

    def obter_dados_da_coluna(self):
        # Conectar ao banco de dados
        self.conectar_banco_de_dados()

        # Definir a consulta SQL para selecionar a coluna 'simbolo'
        consulta_sql = f"SELECT {self.coluna} FROM {self.tabela}"

        # Executar a consulta SQL
        self.cursor.execute(consulta_sql)

        # Buscar todos os resultados da coluna 'simbolo'
        resultados = self.cursor.fetchall()

        # Criar a lista de símbolos
        dados_da_coluna = [resultado[0] for resultado in resultados]

        # Desconectar do banco de dados
        self.desconectar_banco_de_dados()

        # Retornar a lista de símbolos
        return dados_da_coluna
