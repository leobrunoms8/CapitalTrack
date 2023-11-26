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

    def executar_consulta(self, encontrados):
        self.encontrados = encontrados
        resultados = []

        self.conectar_banco_de_dados()
        
        for string in self.encontrados:
            consulta_sql = f"SELECT simbolo, nome_da_empresa FROM raspagem WHERE simbolo = '{string}'"

            self.cursor.execute(consulta_sql)

            resultado = self.cursor.fetchall()

            if resultado:
                simbolo, nome_empresa = resultado[0] if resultado else (None, None)
                resultados.append({
                    simbolo,
                    nome_empresa
                })

        # Desconectar do banco de dados
        self.desconectar_banco_de_dados()

        return resultados

