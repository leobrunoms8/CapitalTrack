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

        # Coletar lista de Id contida na tabela Index_de_acoes    
        consulta_sql = "SELECT id FROM index_de_acoes"
        self.cursor.execute(consulta_sql)
        lista_de_id = [id[0] for id in self.cursor.fetchall()]

        for resultado in resultados:
            if len(resultado) == 2:
                simbolo, nome_da_empresa = resultado

                # Verificar se o símbolo já existe na tabela
                consulta_sql = "SELECT id FROM index_de_acoes WHERE simbolo = %s"
                self.cursor.execute(consulta_sql, (simbolo,))
                existe_simbolo = self.cursor.fetchone()

                if existe_simbolo:
                    print(f"O símbolo {simbolo} já está contido na lista index_de_acoes.")
                else:
                    # Verificar se o símbolo já existe na coluna nome_da_empresa
                    consulta_sql = "SELECT id FROM index_de_acoes WHERE nome_da_empresa = %s"
                    self.cursor.execute(consulta_sql, (nome_da_empresa,))
                    existe_empresa = self.cursor.fetchone()

                    if existe_empresa:
                        print(f"O símbolo {simbolo} já está contido na lista index_de_acoes, e na coluna errada. Observe o id: {existe_empresa[0]}")
                    else:
                        # Insere a linha se o símbolo não existe
                        self.cursor.execute("""
                            INSERT INTO index_de_acoes (simbolo, nome_da_empresa)
                            VALUES (%s, %s)
                        """, (simbolo, nome_da_empresa))
                        self.conexao.commit()
                        print(f"Linha {simbolo} inserida com sucesso.")
            else:
                print(f"Resultado inválido: {resultado}")


        # Desconectar Banco de Dados
        self.fechar_conexao()
