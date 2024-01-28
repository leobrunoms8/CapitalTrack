import yfinance as yf
import mysql.connector
import pandas as pd
from io import StringIO

class Testagem_Yfinance:
    def __init__(self):
        self



    def testagem_por_data_encontrados(self, data_ex):
        
        try:
            # Define o dia de hoje
            tabela_nome = f"`tabela_{data_ex}`"

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
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
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT simbolo FROM {tabela_nome}")
            simbolo_p_analisar_hoje = cursor.fetchall()

            # Remover caracteres '(', ')', e ',' de cada string
            simbolo_p_analisar_hoje_formatados = [simbolo[0].replace('(', '').replace(')', '').replace(',', '') for simbolo in simbolo_p_analisar_hoje]

            simbolos_nao_encontrados_primeira_tentativa = []
            simbolos_nao_encontrados_segunda_tentativa = []

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
                    except Exception as e:
                        # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                        print(f"Erro ao consultar simbolo {simbolo}: {e}")
                        simbolos_nao_encontrados_segunda_tentativa.append(simbolo)
                        simbolos_nao_encontrados_primeira_tentativa.remove(simbolo)
                        continue

        finally:
            return simbolos_nao_encontrados_primeira_tentativa  
    
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
        try:
            print("Analisando: '",simbolo,"'")

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

            print(frequencia_dividendos)

            frequencia_dividendos_tratada = self.extrair_frequencia_dividendos(frequencia_dividendos)

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
                print('A frequência é mensal.')
            elif 80 <= frequencia_moda.days <= 100:
                print('A frequência é trimestral.')
            elif 350 <= frequencia_moda.days <= 400:
                print('A frequência é anual.')
            else:
                print('A frequência não está definida ou é irregular.')
                
                # Identificar os meses mais comuns na lista de datas
                meses_mais_comuns = dados_df.index.month.value_counts().index.tolist()
                print(f'Meses mais comuns na lista: {meses_mais_comuns}')




            
            return frequencia_dividendos_tratada

        except Exception as e:
            # Se ocorrer um erro, exibe o erro e continua
            print(f"Erro ao consultar simbolo {simbolo}: {e}")
    
    def testagem_moeda_da_acao(self, simbolo):
        try:
            print("Analisando: '",simbolo,"'")

            # Tenta criar um objeto Ticker para o símbolo
            acao = yf.Ticker(simbolo)

            # Tenta obter as informações importantes da ação
            # Moeda da ação

            fast_info = acao.get_fast_info()
            moeda = fast_info['currency']

            return moeda

        except Exception as e:
            # Se ocorrer um erro, exibe o erro e continua
            print(f"Erro ao consultar simbolo {simbolo}: {e}")

    def extrair_frequencia_dividendos(self, dividendos_acao):
        try:
            # Converte a string para um DataFrame
            df = pd.read_csv(StringIO(dividendos_acao), delim_whitespace=True)

            # Converte a coluna 'Date' para datetime
            df['Date'] = pd.to_datetime(df['Date'])

            # Calcula a diferença entre datas consecutivas
            diferenca_datas = df['Date'].diff().dt.total_seconds()

            # Calcula a moda da diferença para obter a frequência mais comum
            frequencia = diferenca_datas.mode().iloc[0]

            return frequencia

        except Exception as e:
            # Se ocorrer um erro, exibe o erro e continua
            print(f"Erro ao extrair frequência de dividendos: {e}")
            return None
    
    def extrair_relacao_dividendo_valor_da_acao(self, simbolo, data_ex, valor_da_acao):
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Configura o nome da tabela
            tabela = 'tabela_' + data_ex
            print(tabela)
            print(simbolo)

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            consulta_sql = """
                SELECT
                    valor_dividendo
                FROM
                    %s
                WHERE
                    simbolo = %s
            """
            cursor.execute(consulta_sql, (tabela, simbolo,))

            dividendo = cursor.fetchall()

            # Verifica se há resultados
            if dividendo:
                relacao_dividendo_valor_da_acao = dividendo[0][0] / valor_da_acao
            else:
                relacao_dividendo_valor_da_acao = None

        except Exception as e:
            print(f"Erro ao consultar simbolo {simbolo}: {e}")
            relacao_dividendo_valor_da_acao = None

        finally:
            cursor.close()
            db.close()
            return relacao_dividendo_valor_da_acao
