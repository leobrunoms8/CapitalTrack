import mysql.connector

class GerenciadorTabelaAcoes:
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

    def criar_tabela(self):
        try:
            # Estabelece a conexão com o servidor MySQL e seleciona o banco de dados "Stocks"
            self.conectar_banco_de_dados()

            # Comando SQL para criar a tabela com as colunas desejadas
            criar_tabela_sql = """
            CREATE TABLE IF NOT EXISTS index_de_acoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simbolo VARCHAR(255) NOT NULL,
                nome_da_empresa VARCHAR(255) NOT NULL,
                UNIQUE (simbolo)
            )
            """
            self.cursor.execute(criar_tabela_sql)

            print("Tabela 'index_de_acoes' criada com sucesso.")

        except mysql.connector.Error as erro:
            print(f"Erro ao criar a tabela: {erro}")

        finally:
            if self.conexao is not None and self.conexao.is_connected():
                self.cursor.close()
                self.conexao.close()
                print("Conexão encerrada.")

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()

    def inserir_linha(self, resultados):
        self.conectar_banco_de_dados()

        for resultado in resultados:
            if len(resultado) == 2:
                simbolo, nome_da_empresa = resultado
                # Verifica se o símbolo já existe na tabela
                self.cursor.execute("SELECT * FROM index_de_acoes WHERE simbolo = %s", (simbolo,))
                result = self.cursor.fetchone()

                if result is None:
                    # Insere a linha se o símbolo não existe
                    self.cursor.execute("""
                        INSERT INTO index_de_acoes (simbolo, nome_da_empresa)
                        VALUES (%s, %s)
                    """, (simbolo, nome_da_empresa))
                    self.conexao.commit()
                    print(f"Linha {simbolo} inserida com sucesso.")
                else:
                    print(f"O símbolo {simbolo} já existe na tabela.")
            else:
                print(f"Resultado inválido: {resultado}")

        # Desconectar Banco de Dados
        self.fechar_conexao()

    