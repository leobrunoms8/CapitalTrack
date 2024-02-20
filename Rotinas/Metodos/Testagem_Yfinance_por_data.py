import yfinance as yf
import mysql.connector
import pandas as pd
from io import StringIO
from .Atualizar_Tabelas import Atualizar_Tabelas

class Testagem_Yfinance:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self



    def testagem_por_data_encontrados(self, data_ex):
        
        try:
            # Define o dia de hoje
            tabela_nome = f"`tabela_{data_ex}`"

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT simbolo FROM {tabela_nome}")
            simbolo_p_analisar_hoje = cursor.fetchall()

            # Remover caracteres '(', ')', e ',' de cada string
            simbolo_p_analisar_hoje_formatados = [simbolo[0].replace('(', '').replace(')', '').replace(',', '') for simbolo in simbolo_p_analisar_hoje]

            simbolos_encontrados = []

            for simbolo in simbolo_p_analisar_hoje_formatados:
                try:
                    # Imprime qual Siímbolo está sendo Analisado no momento

                    print("Analisando: '",simbolo,"'")

                    # Tenta criar um objeto Ticker para o símbolo
                    acao = yf.Ticker(simbolo)

                    # Obtém os dados históricos mais recentes (último dia)
                    dados_historicos = acao.history(period='1d')

                    # Obtém o preço de fechamento mais recente
                    ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
                    # print(ultimo_preco_fechamento)
                    print(ultimo_preco_fechamento)

                    # Adiciona o símbolo aos símbolos encontrados
                    simbolos_encontrados.append(simbolo)
                    
                except Exception as e:
                        # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                        print(f"Erro ao consultar simbolo {simbolo}: {e}")
                        continue
        finally:
            return simbolos_encontrados
    
    def testagem_por_data_nao_encontrados(self, data_ex):
        
        try:
            # Define o dia de hoje
            tabela_nome = f"`tabela_{data_ex}`"

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT simbolo FROM {tabela_nome}")
            simbolo_p_analisar_hoje = cursor.fetchall()

            # Remover caracteres '(', ')', e ',' de cada string
            simbolo_p_analisar_hoje_formatados = [simbolo[0].replace('(', '').replace(')', '').replace(',', '') for simbolo in simbolo_p_analisar_hoje]

            simbolos_nao_encontrados_primeira_tentativa = []
            simbolos_encontrados_com_sa = []

            for simbolo in simbolo_p_analisar_hoje_formatados:
                try:
                    # Tenta criar um objeto Ticker para o símbolo
                    acao = yf.Ticker(simbolo)

                    # Obtém os dados históricos mais recentes (último dia)
                    dados_historicos = acao.history(period='1d')

                    # Obtém o preço de fechamento mais recente
                    ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
                    
                except Exception as e:
                        # Caso não encontre em uma primeira tentativa é incluido na lista de não encontrados
                        simbolos_nao_encontrados_primeira_tentativa.append(simbolo)
                        continue
            
            for simbolo in simbolos_nao_encontrados_primeira_tentativa:
                    try:
                        # Imprime qual Siímbolo está sendo Analisado no momento

                        print("Analisando: '",simbolo,"'")

                        # Tenta criar um objeto Ticker para o símbolo
                        acao = yf.Ticker(simbolo + '.SA')

                        # Obtém os dados históricos mais recentes (último dia)
                        dados_historicos = acao.history(period='1d')

                        # Obtém o preço de fechamento mais recente
                        ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
                        print(ultimo_preco_fechamento)
                        
                        simbolos_encontrados_com_sa.append(simbolo)
                    except Exception as e:
                        # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                        print(f"Erro ao consultar simbolo {simbolo}: {e}")
                        continue

        finally: 
            return simbolos_encontrados_com_sa 
    
    def testagem_preco(self, simbolo):
        try:
            # Imprime qual Siímbolo está sendo Analisado no momento

            print("Analisando: '",simbolo,"'")

            # Tenta criar um objeto Ticker para o símbolo
            acao = yf.Ticker(simbolo)

            # Obtém os dados históricos mais recentes (último dia)
            dados_historicos = acao.history(period='1d')

            # Obtém o preço de fechamento mais recente
            ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]

            return ultimo_preco_fechamento
            
        except Exception as e:
            # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
            print(f"Erro ao consultar simbolo {simbolo}: {e}")
             
    def testagem_frequencia_de_dividendos(self, simbolo):
        frequencia_dividendos_tratada = ''
        try:
            print("Analisando a frequencia de dividendos de: '",simbolo,"'")

            # Tenta criar um objeto Ticker para o símbolo
            acao = yf.Ticker(simbolo)

            # Tenta obter as informações importantes da ação
            # Dividendos

            dividendos_acao = acao.get_dividends()

            # Trabalhar para extrair a frequencia

            string_parcialmente_pronta = dividendos_acao.to_string(index=True, header=True)

            # Remova a palavra "Date"
            string_parcialmente_pronta_1 = string_parcialmente_pronta.replace("Date", "")

            # Remova a parte específica
            string_parcialmente_pronta_2 = string_parcialmente_pronta_1.replace("00:00:00-04:00", "")

            # Remova a parte específica
            frequencia_dividendos = string_parcialmente_pronta_2.replace("00:00:00-05:00", "")

            # Converter a string para um DataFrame do pandas
            dados_df = pd.read_csv(StringIO(frequencia_dividendos), delim_whitespace=True, names=['Date', 'Value'], index_col='Date')

            # Converter o índice para o tipo datetime
            dados_df.index = pd.to_datetime(dados_df.index)

            # Calcular a diferença entre as datas
            diferencas = dados_df.index.to_series().diff()

            # Identificar a moda das diferenças (pode haver múltiplos valores se a frequência não for constante)
            frequencia_moda = diferencas.mode().iloc[0]

            # Imprimir a moda das diferenças
            print(f'Moda das diferenças entre as datas: {frequencia_moda}')

            # Verificar se a frequência é mensal, trimestral, anual ou sem frequência definida
            if 20 <= frequencia_moda.days <= 40:
                frequencia_dividendos_tratada = 'mensal'
                print('A frequência é ', frequencia_dividendos_tratada, '.')
            elif 80 <= frequencia_moda.days <= 100:
                frequencia_dividendos_tratada = 'trimestral'
                print('A frequência é ', frequencia_dividendos_tratada, '.')
            elif 350 <= frequencia_moda.days <= 400:
                frequencia_dividendos_tratada = 'anual'
                print('A frequência é ', frequencia_dividendos_tratada, '.')
            else:
                frequencia_dividendos_tratada = 'irregular'
                print('A frequência não está definida ou é ', frequencia_dividendos_tratada, '.')
     
            return frequencia_dividendos_tratada

        except Exception as e:
            # Se ocorrer um erro, exibe o erro e continua
            print(f"Erro ao consultar os dividendos da ação {simbolo}: {e}")
    
    def testagem_moeda_da_acao(self, simbolo):
        moeda = ''
        try:
            print("Analisando a modea da ação: '",simbolo,"'")

            # Tenta criar um objeto Ticker para o símbolo
            acao = yf.Ticker(simbolo)

            # Tenta obter as informações importantes da ação
            # Moeda da ação

            fast_info = acao.get_fast_info()
            moeda = fast_info['currency']
            print(moeda)

            return moeda

        except Exception as e:
            # Se ocorrer um erro, exibe o erro e continua
            print(f"Erro ao consultar a moeda da ação {simbolo}: {e}")
   
    def extrair_relacao_dividendo_valor_da_acao(self, tabela, simbolo, valor_da_acao):
        relacao_dividendo_valor_da_acao = None
        print("Analisando a relação de dividendos por valor da ação de: '",simbolo,"'")
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente ao símbolo escolhido
            consulta_sql = f"SELECT valor_dividendo FROM {tabela} WHERE simbolo = %s"
            cursor.execute(consulta_sql, (simbolo,))

            resultados_dos_valores = cursor.fetchone()
            print(resultados_dos_valores)
            dividendo = self.conversao_de_dividendos(resultados_dos_valores)

            print(dividendo)
            print(valor_da_acao)
            relacao_dividendo_valor_da_acao = dividendo / valor_da_acao
            relacao_final = relacao_dividendo_valor_da_acao * 100
            print(relacao_final)


        except mysql.connector.Error as e:
            print(f"Erro ao consultar a relação de dividendos por valor da ação de: {simbolo}: {e}")

        finally:
            cursor.close()
            db.close()
            return relacao_dividendo_valor_da_acao
        
    def conversao_de_dividendos(self, resultados_dos_valores):
        # Encontrar a posição da primeira vírgula
        primeira_virgula = str(resultados_dos_valores).find(',')
        
        # Encontrar a posição da segunda vírgula a partir da posição da primeira vírgula
        segunda_virgula = str(resultados_dos_valores).find(',', primeira_virgula + 1)

        # Criar uma nova string excluindo-a
        nova_string = str(resultados_dos_valores)[:segunda_virgula] + str(resultados_dos_valores)[segunda_virgula+1:]

        # Remova caracteres desnecessários
        string_limpa = nova_string.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "")

        # Substitua a vírgula pelo ponto como separador decimal
        string_numerica = string_limpa.replace(',', '.')

        # Converta a string numérica para float
        try:
            numero_float = float(string_numerica)
        except ValueError as erro:
            print(string_numerica)
        finally:
            return numero_float
    
    def testagem_automatica(self, data_ex):
        # Define o dia de hoje
        tabela_nome = f"`tabela_{data_ex}`"

        # Conecte ao banco de dados MySQL
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        cursor = db.cursor()

        # Execute uma consulta para obter dados da tabela correspondente à data escolhida
        cursor.execute(f"SELECT simbolo FROM {tabela_nome}")
        simbolo_p_analisar_hoje = cursor.fetchall()

        # Remover caracteres '(', ')', e ',' de cada string
        simbolo_p_analisar_hoje_formatados = [simbolo[0].replace('(', '').replace(')', '').replace(',', '') for simbolo in simbolo_p_analisar_hoje]

        simbolos_encontrados_primeira_tentativa = []
        simbolos_encontrados_segunda_tentativa = []
        simbolos_nao_encontrados =[]
        valor_dinamico = []
        self.atualizacao = Atualizar_Tabelas(self.host, self.user, self.password, self.database)

        cursor.close()
        db.close()

        for simbolo in simbolo_p_analisar_hoje_formatados:
            frequencia = None
            moeda = None
            relacao = None
            ultimo_preco_fechamento = None
            try:
                # Imprime qual Siímbolo está sendo Analisado no momento

                print("Analisando: '",simbolo,"'")

                # Tenta criar um objeto Ticker para o símbolo
                acao = yf.Ticker(simbolo)

                # Obtém os dados históricos mais recentes (último dia)
                dados_historicos = acao.history(period='1d')

                # Obtém o preço de fechamento mais recente
                ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]

                valor_dinamico.append((simbolo, ultimo_preco_fechamento))

            except Exception as e:
                    # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                    print(f"Erro ao consultar simbolo {simbolo}: {e}")
                    try:
                        # Imprime qual Siímbolo está sendo Analisado no momento

                        simbolo_BRL = simbolo + '.SA'

                        print("Analisando: '",simbolo_BRL,"'")

                        # Tenta criar um objeto Ticker para o símbolo
                        acao = yf.Ticker(simbolo_BRL)

                        # Obtém os dados históricos mais recentes (último dia)
                        dados_historicos = acao.history(period='1d')
                        # Obtém o preço de fechamento mais recente
                        ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
                        # print(ultimo_preco_fechamento)
                        print(ultimo_preco_fechamento)

                        valor_dinamico.append((simbolo, ultimo_preco_fechamento))

                    except Exception as e:
                        print(f"Erro ao consultar simbolo {simbolo} na segunda tentativa com .SA: {e}")
                        simbolos_nao_encontrados.append(simbolo)
                    
                    try:
                        # Adiciona o símbolo aos símbolos encontrados
                        simbolos_encontrados_segunda_tentativa.append(simbolo)
                        frequencia = self.testagem_frequencia_de_dividendos(simbolo_BRL)
                        self.atualizacao.atualizar_tabela_dividendos_frequencia(tabela_nome, simbolo, frequencia)
                        moeda = self.testagem_moeda_da_acao(simbolo_BRL)
                        self.atualizacao.atualizar_tabela_dividendos_moeda(tabela_nome, simbolo, moeda)
                        relacao = self.extrair_relacao_dividendo_valor_da_acao(tabela_nome, simbolo, ultimo_preco_fechamento)
                        self.atualizacao.atualizar_tabela_dividendos_relacao(tabela_nome, simbolo, relacao)
                    except Exception as e:
                        # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                        print(f"Erro ao consultar simbolo {simbolo} na segunda tentativa com .SA: {e}")
                    continue
            try:
                # Adiciona o símbolo aos símbolos encontrados
                simbolos_encontrados_primeira_tentativa.append(simbolo)
                frequencia = self.testagem_frequencia_de_dividendos(simbolo)
                self.atualizacao.atualizar_tabela_dividendos_frequencia(tabela_nome, simbolo, frequencia)
                moeda = self.testagem_moeda_da_acao(simbolo)
                self.atualizacao.atualizar_tabela_dividendos_moeda(tabela_nome, simbolo, moeda)
                relacao = self.extrair_relacao_dividendo_valor_da_acao(tabela_nome, simbolo, ultimo_preco_fechamento)
                self.atualizacao.atualizar_tabela_dividendos_relacao(tabela_nome, simbolo, relacao)
                print('Execução Automática concluída')
            except Exception as e:
                # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                print(f"Erro ao consultar simbolo {simbolo} na primeira tentativa: {e}")
                continue
        print(valor_dinamico)    
        return valor_dinamico

            
