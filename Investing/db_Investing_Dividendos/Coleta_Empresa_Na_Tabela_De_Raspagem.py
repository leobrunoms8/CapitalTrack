import mysql.connector

class Coleta_Empresa_Na_Tabela_De_Raspagem:
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

    def desconectar_banco_de_dados(self):
        # Fechar o cursor e a conexão com o banco de dados
        self.cursor.close()
        self.conexao.close()

    def obter_lista_de_empresa(self):
        # Conectar ao banco de dados
        self.conectar_banco_de_dados()

        # Definir a consulta SQL para selecionar a coluna 'nome da empresa'
        consulta_sql = f"SELECT nome_da_empresa FROM {self.tabela}"

        # Executar a consulta SQL
        self.cursor.execute(consulta_sql)

        # Buscar todos os resultados da coluna 'simbolo'
        resultados = self.cursor.fetchall()

        # Criar a lista de símbolos
        lista_de_empresa = [resultado[0] for resultado in resultados]

        # Desconectar do banco de dados
        self.desconectar_banco_de_dados()

        # Retornar a lista de símbolos
        return lista_de_empresa
