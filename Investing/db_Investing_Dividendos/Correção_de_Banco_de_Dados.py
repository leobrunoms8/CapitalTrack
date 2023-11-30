import mysql.connector
import yfinance as yf

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
            consulta_sql = f"SELECT id FROM {self.tabela}"

            # Executar a consulta SQL
            self.cursor.execute(consulta_sql)

            lista_de_id = self.cursor.fetchall()

            # Iterar sobre os símbolos e inverter as informações se o nome_da_empresa estiver em maiúsculo
            for (id,) in lista_de_id:
                # Inicializa simbolo fora do bloco try
                simbolo = None
                
                # Consulta API yfinance para obter informações do ticker
                try:
                    # Consulta o simbolo correspondente ao id
                    consulta_simbolo = f"SELECT simbolo FROM {self.tabela} WHERE id = %s"

                    self.cursor.execute(consulta_simbolo, (id,))
                    simbolo_tupla = self.cursor.fetchone()

                    if simbolo_tupla:
                        simbolo = simbolo_tupla[0]
                        print("Analisando:", simbolo)

                        # Tenta criar um objeto Ticker para o símbolo
                        acao = yf.Ticker(simbolo)

                        # Obtém os dados históricos mais recentes (último dia)
                        dados_historicos = acao.history(period='1d')

                        # Obtém o preço de fechamento mais recente
                        ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
                        print(ultimo_preco_fechamento)

                except Exception as e:
                    print(f"Erro: {e}")

                    # Consulta SQL para obter informações atuais do id especificado
                    consulta_atual = f"SELECT id, simbolo, nome_da_empresa FROM {self.tabela} WHERE id = %s"
                    self.cursor.execute(consulta_atual, (id,))
                    resultado_atual = self.cursor.fetchone()

                    if resultado_atual:
                        _, simbolo, nome_da_empresa = resultado_atual

                        # Atualizar a linha no banco de dados trocando simbolo e nome_da_empresa
                        atualizar_query = f"UPDATE {self.tabela} SET simbolo = %s, nome_da_empresa = %s WHERE id = %s"
                        valores = (nome_da_empresa, simbolo, id)
                        self.cursor.execute(atualizar_query, valores)

                        # Commit e fechar o cursor
                        self.conexao.commit()

                        print(f"As informações para o ID {id} foram trocadas com sucesso.")
                    else:
                        print(f"Nenhum registro encontrado para o ID {id}.")

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            # Desconectar do banco de dados
            self.fechar_conexao()

