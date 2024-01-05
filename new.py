
from forex_python.converter import CurrencyRates
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidgetItem, QMessageBox
from datetime import datetime, timedelta


from .FrontEnd.Interface.Window_Dividendos import Ui_Dividendos

import yfinance as yf
import mysql.connector

def analisar_dividendos_por_rel_div_val_aca_hoje(self):
            # Verifique se hoje é sábado ou domingo
            hoje = datetime.now()
            dia_semana = hoje.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

            if dia_semana == 5 or dia_semana == 6:  # 5 é sábado, 6 é domingo
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
            
            try:
                # Define o dia de hoje
                data_hoje = hoje.strftime("%d.%m.%Y")
                tabela_nome = f"`tabela_{data_hoje}`"

                # Conecte ao banco de dados MySQL
                db = mysql.connector.connect(
                    host="localhost",
                    user="developer",
                    password="Leo140707",
                    database="RaspagemPuraDeDados"
                )

                cursor = db.cursor()

                # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                cursor.execute(f"SELECT * FROM {tabela_nome}")

                # Recupere os resultados
                resultados = cursor.fetchall()
                numero_de_resultados = len(resultados)
                print(numero_de_resultados)

                cursor.execute(f"SELECT simbolo FROM {tabela_nome}")
                simbolo_p_analisar_hoje = cursor.fetchall()

                # Remover caracteres '(', ')', e ',' de cada string
                simbolo_p_analisar_hoje_formatados = [simbolo[0].replace('(', '').replace(')', '').replace(',', '') for simbolo in simbolo_p_analisar_hoje]

                simbolos_encontrados = []
                simbolos_nao_encontrados = []

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
                        print(ultimo_preco_fechamento)

                        # Adiciona o símbolo aos símbolos encontrados
                        simbolos_encontrados.append(simbolo)
                        
                    except Exception as e:
                            # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                            print(f"Erro ao consultar simbolo {simbolo}: {e}")
                            simbolos_nao_encontrados.append(simbolo)
                            continue

                    print('Símbolos Encontrados')
                    print(simbolos_encontrados)
                    print('Símbolos não Encotrados')
                    print(simbolos_nao_encontrados)

                # -------------- Dropar tabela racunho ----------
                try: 
                    # Estabelece a conexão com o servidor MySQL e seleciona o banco de dados "Stocks"
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="developer",
                        password="Leo140707",
                        database="RaspagemPuraDeDados"
                    )

                    # Criar um cursor para executar consultas SQL
                    cursor = conn.cursor()

                    # Substitua "sua_tabela" pelo nome da tabela que você deseja apagar
                    tabela_a_apagar = 'rascunho'

                    # Comando SQL para apagar a tabela
                    query = f"DROP TABLE {tabela_a_apagar}"

                    # Executar o comando SQL
                    cursor.execute(query)

                    # Commit para salvar as alterações no banco de dados
                    conn.commit()

                    print('Tabela rascunho dropada')
                except mysql.connector.Error as erro:
                    print(f"Erro ao dropar a tabela: {erro}")


                # Fechar o cursor e a conexão
                cursor.close()
                conn.close()

                # ----------------- Criar tabela rascunho --------------
                conexao = None
                try:
                    # Estabelece a conexão com o servidor MySQL e seleciona o banco de dados "Stocks"
                    conexao = mysql.connector.connect(
                        host="localhost",
                        user="developer",
                        password="Leo140707",
                        database="RaspagemPuraDeDados"
                    )

                    # Cria um cursor para executar comandos SQL
                    cursor = conexao.cursor()

                    # Comando SQL para criar a tabela com as colunas desejadas
                    criar_tabela_sql = """
                    CREATE TABLE IF NOT EXISTS rascunho (
                        simbolo VARCHAR(255) NOT NULL,
                        nome_da_empresa VARCHAR(255) NOT NULL,
                        data_ex DATE NOT NULL,
                        moeda VARCHAR(255) NOT NULL,
                        valor_dividendo DECIMAL(7, 6) NOT NULL,
                        valor_em_BRL DECIMAL(7, 6) NOT NULL,
                        frequencia VARCHAR(50) NOT NULL,
                        data_pagamento DATE NOT NULL,
                        percentual_acao DECIMAL(7, 6) NOT NULL
                    )
                    """
                    cursor.execute(criar_tabela_sql)

                    print("Tabela 'rascunho' criada com sucesso.")

                except mysql.connector.Error as erro:
                    print(f"Erro ao criar a tabela: {erro}")

                finally:
                    if conexao is not None and conexao.is_connected():
                        cursor.close()
                        conexao.close()
                        print("Conexão encerrada.")          

                # Pegar linha a linha de acordo com a lista de encontrados
                
                for simbolo in simbolos_encontrados:
                    try:
                        print(simbolo)
                        # Conecte ao banco de dados MySQL
                        db = mysql.connector.connect(
                            host="localhost",
                            user="developer",
                            password="Leo140707",
                            database="RaspagemPuraDeDados"
                        )

                        cursor = db.cursor()

                        # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                        cursor.execute(f"SELECT valor_dividendo FROM {tabela_nome} WHERE simbolo = '{simbolo}'")

                        # Recupere os resultados
                        resultados_dos_valores = cursor.fetchall()
                        print(resultados_dos_valores)

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
                            continue


                        print(numero_float)

                        # Consulta a moeda do dividendo
                        # Tenta criar um objeto Ticker para o símbolo
                        acao = yf.Ticker(simbolo)

                        # Tenta obter as informações importantes da ação
                        # Moeda da ação

                        fast_info = acao.get_fast_info()
                        moeda = fast_info['currency']
                        print(moeda)
                        if moeda == 'USD':
                            # Multiplicar pela cotação atual
                            # Criar um objeto CurrencyRates
                            c = CurrencyRates()

                            # Obter a taxa de câmbio USD para BRL
                            taxa_usd_brl = c.get_rate('USD', 'BRL')

                            # Imprimir a taxa de câmbio
                            print(f"A taxa de câmbio USD/BRL é: {taxa_usd_brl}")

                            dividendo_em_BRL = taxa_usd_brl * numero_float
                            print(f'O valor do dividendo em reais é: {dividendo_em_BRL}')

                            
                        elif moeda == 'BRL':
                            # Apenas imprimir na tela
                            print(numero_float)
                        
                        # Relação Dividendo/Ação
                        # Obtém os dados históricos mais recentes (último dia)
                        dados_historicos = acao.history(period='1d')

                        # Obtém o preço de fechamento mais recente
                        preco_acao = dados_historicos['Close'].iloc[-1]

                        relacao_div_acao = numero_float / preco_acao

                        print(relacao_div_acao)
                            
                    except mysql.connector.Error as erro:
                        print(f"Erro ao consultar a tabela: {erro}")
                # Anexar as novas informações a tabela rascunho
                    try:
                        # Conecte ao banco de dados MySQL
                        db = mysql.connector.connect(
                            host="localhost",
                            user="developer",
                            password="Leo140707",
                            database="RaspagemPuraDeDados"
                        )

                        cursor = db.cursor()

                        # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                        cursor.execute(f"SELECT id, nome_empresa, data_ex, data_pagamento FROM {tabela_nome} WHERE simbolo = '{simbolo}'")

                        # Recupere os resultados
                        resultados_dos_valores = cursor.fetchall()
                        print(resultados_dos_valores)

                    except mysql.connector.Error as erro:
                        print(f"Erro ao consultar a tabela: {erro}")

                        

                
                        
                



                for simbolo in simbolos_encontrados:
                    try:
                        print("Analisando: '",simbolo,"'")

                        # Tenta criar um objeto Ticker para o símbolo
                        acao = yf.Ticker(simbolo)

                        # Tenta obter as informações importantes da ação
                        # Moeda da ação

                        fast_info = acao.get_fast_info()
                        moeda = fast_info['currency']
                        print(moeda)

                        # Dividendos

                        dividendos_acao = acao.get_dividends()
                        print(dividendos_acao)

                    except Exception as e:
                        # Se ocorrer um erro, exibe o erro e continua
                        print(f"Erro ao consultar simbolo {simbolo}: {e}")
                        continue

                    # Preencha a tabela na janela de "Dividendos"
                    self.ui_dividendos.tableWidget_6.setRowCount(len(resultados))
                    for row_index, row_data in enumerate(resultados):
                        for col_index, col_data in enumerate(row_data):
                            item = QTableWidgetItem(str(col_data))
                            self.ui_dividendos.tableWidget_6.setItem(row_index, col_index, item)

            except mysql.connector.Error as err:
                # Handle the error (e.g., table not found)
                print(f"Error: {err}")

            finally:
                # Feche a conexão com o banco de dados
                db.close()

    def atualizar_progressbar(self, identificador, valor_atual, valor_total):
        # Encontrar a QProgressBar correspondente usando o identificador
        progress_bar = getattr(self.ui_dividendos, identificador)

        # Calcular o valor percentual
        percentual = int((valor_atual / valor_total) * 100)

        # Atualizar a barra de progresso
        progress_bar.setValue(percentual)
            
    def switch_case_numero_dia_da_semana0(self, argument):
        switch_dict = {
            0: 7,
            1: 6,
            2: 5,
            3: 4,
            4: 3,
            5: 2,
            6: 1,
        }

        return switch_dict.get(argument, 'Esta é a execução padrão')

    def switch_case_numero_dia_da_semana1(self, argument):
        switch_dict = {
            0: 14,
            1: 13,
            2: 12,
            3: 11,
            4: 10,
            5: 9,
            6: 8,
        }
    
        return switch_dict.get(argument, 'Esta é a execução padrão')
    
    def switch_case_numero_dia_da_semana2(self, argument):
        switch_dict = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
        }

        return switch_dict.get(argument, 'Esta é a execução padrão')
