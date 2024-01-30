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
                print('A frequência é mensal.')
            elif 80 <= frequencia_moda.days <= 100:
                frequencia_dividendos_tratada = 'trimestral'
                print('A frequência é trimestral.')
            elif 350 <= frequencia_moda.days <= 400:
                frequencia_dividendos_tratada = 'anual'
                print('A frequência é anual.')
            else:
                frequencia_dividendos_tratada = 'irregular'
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
   
    def extrair_relacao_dividendo_valor_da_acao(self, tabela, simbolo, valor_da_acao):
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente ao símbolo escolhido
            consulta_sql = f"SELECT valor_dividendo FROM `{tabela}` WHERE simbolo = %s"
            cursor.execute(consulta_sql, (simbolo,))

            resultados_dos_valores = cursor.fetchone()
            print(resultados_dos_valores)
            dividendo = self.conversao_de_dividendos(resultados_dos_valores)


            # Verifica se há resultados
            if dividendo:
                print(dividendo)
                print(valor_da_acao)
                relacao_dividendo_valor_da_acao = dividendo / valor_da_acao
            else:
                relacao_dividendo_valor_da_acao = None

        except mysql.connector.Error as e:
            print(f"Erro ao consultar símbolo {simbolo}: {e}")
            relacao_dividendo_valor_da_acao = None

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
            
