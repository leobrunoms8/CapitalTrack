from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableWidgetItem, QMessageBox, QWidget, QPushButton, QProgressBar, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QDate
from PyQt5 import QtCore, QtGui, QtWidgets
from FrontEnd.Interface.Window_Main import Ui_MainWindow
from FrontEnd.Interface.Window_Listas import Ui_Listas
from FrontEnd.Interface.Window_Dividendos import Ui_Dividendos
from Investing.RasparDados import RaspagemInvesting
from datetime import datetime, timedelta
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from forex_python.converter import CurrencyRates

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql
import yfinance as yf
import mysql.connector
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create an instance of the main window design class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect menu item signals to corresponding functions
        self.ui.actionTela_Cheia.triggered.connect(self.exibir_tela_cheia)
        self.ui.actionListas.triggered.connect(self.exibir_listas)
        self.ui.actionDividendos.triggered.connect(self.exibir_dividendos)
        self.ui.pushButton.clicked.connect(self.exibir_grafico)  # Conectar o clique do botão ao método

    def exibir_listas(self):
        # Exemplo de uso da classe e do método
        # url = "https://br.investing.com/dividends-calendar/"
        # raspagem = RaspagemInvesting(url)
        # raspagem.realizar_raspagem()

        # Conecte ao banco de dados MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="Leo140707",
            database="RaspagemPuraDeDados"
        )

        cursor = db.cursor()

        # Execute uma consulta para obter dados da tabela "sua_tabela"
        cursor.execute("SELECT * FROM raspagem")

        # Recupere os resultados
        result = cursor.fetchall()

        # Feche a conexão com o banco de dados
        db.close()

        # Exiba os resultados na QTableWidget
        self.ui.listas_window = QDialog()
        self.ui_listas = Ui_Listas()
        self.ui_listas.setupUi(self.ui.listas_window)

        # Limpe as tabelas existentes
        self.ui_listas.tableWidget.setRowCount(0)
        self.ui_listas.tableWidget_2.setRowCount(0)
        self.ui_listas.tableWidget_3.setRowCount(0)

        # Preencha a primeira tabela (Raspagem)
        self.ui_listas.tableWidget.setRowCount(len(result))
        for row_index, row_data in enumerate(result):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.ui_listas.tableWidget.setItem(row_index, col_index, item)

        self.ui.listas_window.show()
        # Conecte o clique do botão à função que executa o código desejado
        self.ui_listas.pushButton_2.clicked.connect(self.executar_raspagem)

    def executar_raspagem(self):
        # Executar ao clicar no pushButton_2
        url = "https://br.investing.com/dividends-calendar/"
        raspagem = RaspagemInvesting(url)
        raspagem.realizar_raspagem()

    def exibir_tela_cheia(self):
        # Implemente a lógica para exibir a tela cheia aqui
        pass

    def exibir_dividendos(self):
        # Exiba a janela de "Dividendos"
        self.ui.dividendos_window = QDialog()
        self.ui_dividendos = Ui_Dividendos()
        self.ui_dividendos.setupUi(self.ui.dividendos_window)

        # Conecte o clique do botão à função que executa o código desejado
        self.ui_dividendos.pushButton.clicked.connect(self.consultar_dividendos)
        self.ui_dividendos.pushButton_3.clicked.connect(self.consultar_dividendos_por_rel_div_val_aca_hoje)
        self.ui_dividendos.pushButton_4.clicked.connect(self.consultar_dividendos_por_rel_div_val_aca_amanha)
        self.ui_dividendos.pushButton_2.clicked.connect(self.consultar_dividendos_por_rel_div_val_aca_ess_sema)
        self.ui_dividendos.pushButton_5.clicked.connect(self.consultar_dividendos_por_rel_div_val_aca_pro_sema)
        self.ui_dividendos.pushButton_9.clicked.connect(self.analisar_dividendos_por_rel_div_val_aca_hoje)

        self.ui.dividendos_window.show()

    def consultar_dividendos_por_rel_div_val_aca_hoje(self):
        # Verifique se hoje é sábado ou domingo
        hoje = datetime.now()
        dia_semana = hoje.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

        if dia_semana == 5 or dia_semana == 6:  # 5 é sábado, 6 é domingo
            # Mostra uma mensagem informando que é fim de semana
            QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
            return
        
        try:
            # Define o dia de hoje
            hoje = datetime.now()
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
            result = cursor.fetchall()

            # Preencha a tabela na janela de "Dividendos"
            self.ui_dividendos.tableWidget_6.setRowCount(len(result))
            for row_index, row_data in enumerate(result):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui_dividendos.tableWidget_6.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()

    def consultar_dividendos_por_rel_div_val_aca_amanha(self):
             # Verifique se hoje é sábado ou domingo
            hoje = datetime.now()
            dia_semana = hoje.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

            if dia_semana == 4 or dia_semana == 5:  # 4 é sexta, 5 é sábado
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
        
            try:
                # Define o dia de amanhã
                hoje = datetime.now()
                dia_amanha = hoje + timedelta(days=1)
                data_amanha = dia_amanha.strftime("%d.%m.%Y")
                tabela_nome = f"`tabela_{data_amanha}`"

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
                result = cursor.fetchall()

                # Preencha a tabela na janela de "Dividendos"
                self.ui_dividendos.tableWidget_3.setRowCount(len(result))
                for row_index, row_data in enumerate(result):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.ui_dividendos.tableWidget_3.setItem(row_index, col_index, item)

            except mysql.connector.Error as err:
                # Handle the error (e.g., table not found)
                print(f"Error: {err}")

            finally:
                # Feche a conexão com o banco de dados
                db.close()
    
    def consultar_dividendos_por_rel_div_val_aca_ess_sema(self):
        try:
            # Define o dia de hoje
            hoje = datetime.now()

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Lista para armazenar os resultados de todas as consultas
            all_results = []

            for i in range(7):  # Loop pelos dias da semana (0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo)
                # Pula os sábados (5) e domingos (6)
                print(i)
                if i == 5 or i == 6:
                    continue

                # Calcula a data para o dia da semana atual
                dia_p_desloc = hoje.weekday()
                desloc = self.switch_case_numero_dia_da_semana2(dia_p_desloc)
                dia_semana_atual = hoje + timedelta(days= i - desloc)
                data_dia_semana_atual = dia_semana_atual.strftime("%d.%m.%Y")
                tabela_nome = f"`tabela_{data_dia_semana_atual}`"

                # Execute a consulta para obter dados da tabela correspondente à data escolhida
                cursor.execute(f"SELECT * FROM {tabela_nome}")

                # Recupere os resultados
                result = cursor.fetchall()

                 # Adicione os resultados à lista
                all_results.extend(result)

                # Preencha a tabela na janela de "Dividendos"
                self.ui_dividendos.tableWidget_4.setRowCount(len(all_results))
                for row_index, row_data in enumerate(all_results):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.ui_dividendos.tableWidget_4.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()

    def consultar_dividendos_por_rel_div_val_aca_pro_sema(self):
        try:
            # Define o dia de hoje
            hoje = datetime.now()

            # Exemplo de uso
            days_number = hoje.weekday()
            end_day = self.switch_case_numero_dia_da_semana1(days_number)
            start_day = self.switch_case_numero_dia_da_semana0(days_number)
            print(start_day, end_day)

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Lista para armazenar os resultados de todas as consultas
            all_results = []

            for i in range(start_day, end_day):  # Loop pelos dias da próxima semana
                
                # Calcula a data para o dia da semana próxima semana
                dia_semana_proxima = hoje + timedelta(days=i)
                data_dia_semana_proxima = dia_semana_proxima.strftime("%d.%m.%Y")
                print(data_dia_semana_proxima)
                tabela_nome = f"`tabela_{data_dia_semana_proxima}`"

                # Pula os sábados (5) e domingos (6)
                conf_data = dia_semana_proxima.weekday()
                if conf_data == 5 or conf_data == 6:
                    continue
                
                try:
                    # Execute a consulta para obter dados da tabela correspondente à data escolhida
                    cursor.execute(f"SELECT * FROM {tabela_nome}")

                    # Recupere os resultados
                    result = cursor.fetchall()

                    # Adicione os resultados à lista
                    all_results.extend(result)

                    # Preencha a tabela na janela de "Dividendos"
                    self.ui_dividendos.tableWidget_5.setRowCount(len(all_results))
                    for row_index, row_data in enumerate(all_results):
                        for col_index, col_data in enumerate(row_data):
                            item = QTableWidgetItem(str(col_data))
                            self.ui_dividendos.tableWidget_5.setItem(row_index, col_index, item)
                except mysql.connector.Error as err:
                    # Handle the error (e.g., table not found)
                    print(f"Error: {err}")
                    continue                

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()

    def consultar_dividendos(self):
        # Obtenha a data escolhida na dateEdit
        data_ex = self.ui_dividendos.dateEdit.date().toString("dd.MM.yyyy")
        tabela_nome = f"`tabela_{data_ex}`"  # Adicione aspas invertidas ao redor do nome da tabela

        # Conecte ao banco de dados MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="Leo140707",
            database="RaspagemPuraDeDados"
        )

        cursor = db.cursor()

        try:
            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT * FROM {tabela_nome}")

            # Recupere os resultados
            result = cursor.fetchall()

            # Preencha a tabela na janela de "Dividendos"
            self.ui_dividendos.tableWidget.setRowCount(len(result))
            for row_index, row_data in enumerate(result):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui_dividendos.tableWidget.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()

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
    
    def exibir_grafico(self):
        try:
            # Conectar ao banco de dados MySQL
            with pymysql.connect(host='localhost', user='developer', password='Leo140707', database='raspagempuradedados') as conexao:
                cursor = conexao.cursor()

                # Obtenha as datas escolhidas nos controles dateEdit e dateEdit_2
                data_inicial = self.ui.dateEdit.date().toString("dd.MM.yyyy")
                data_final = self.ui.dateEdit_2.date().toString("dd.MM.yyyy")

                # Converter as strings para objetos QDate
                qdate_inicial = QDate.fromString(data_inicial, "dd.MM.yyyy")
                qdate_final = QDate.fromString(data_final, "dd.MM.yyyy")

                # Obter as datas como objetos datetime
                data_inicial_datetime = datetime(qdate_inicial.year(), qdate_inicial.month(), qdate_inicial.day())
                data_final_datetime = datetime(qdate_final.year(), qdate_final.month(), qdate_final.day())

                # Converter as datas para o formato "MM.dd.yyyy"
                data_inicial_formatada = data_inicial_datetime.strftime("%m.%d.%Y")
                data_final_formatada = data_final_datetime.strftime("%m.%d.%Y")

                # Crie uma lista de datas entre data_inicial e data_final
                datas_consulta = pd.date_range(data_inicial_formatada, data_final_formatada, freq='D').strftime('%d.%m.%Y').tolist()

                # Inicializar lista para armazenar os resultados
                dados_resultado = []

                for data_ex in datas_consulta:
                    try:
                        # Verificar se a tabela existe antes de executar a consulta SQL
                        tabela_existe = self.verificar_tabela_existente(cursor, data_ex)

                        if tabela_existe:
                            # Consulta SQL para obter os dados da tabela para a data escolhida
                            consulta_sql = f"SELECT data_ex, SUM(CAST(REPLACE(valor_dividendo, ',', '.') AS DECIMAL(10, 4))) as soma_valor_dividendo " \
                                        f"FROM `tabela_{data_ex}` GROUP BY data_ex"

                            # Executar a consulta SQL
                            cursor.execute(consulta_sql)

                            # Obter os resultados e adicionar à lista
                            resultados = cursor.fetchall()

                            if not resultados:
                                # Adicionar algum tratamento ou mensagem para indicar que não há dados para a tabela
                                print(f"Nenhum dado encontrado para a tabela_{data_ex}")
                                continue

                            for resultado in resultados:
                                dados_resultado.append({'data': resultado[0], 'soma_valor_dividendo': resultado[1]})

                    except mysql.connector.Error as err:
                        # Handle the error (e.g., table not found)
                        print(f"Error: {err}")
                        continue

                # Criar DataFrame a partir da lista
                resultado_df = pd.DataFrame(dados_resultado)

                # Substituir '--' por NaN na coluna 'data'
                resultado_df['data'] = resultado_df['data'].replace('--', np.nan)

                # Converter a coluna 'data' para o tipo datetime, ignorando NaN
                resultado_df['data'] = pd.to_datetime(resultado_df['data'], format='%d.%m.%Y', errors='coerce')

                # Classificar DataFrame pela coluna 'data'
                resultado_df = resultado_df.sort_values(by='data')

                # Criar e configurar o gráfico
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(resultado_df['data'], resultado_df['soma_valor_dividendo'])
                ax.set_xlabel('Data Ex')
                ax.set_ylabel('Soma do Valor de Dividendo')
                ax.set_title('Soma do Valor de Dividendo por Data EX')
                plt.xticks(rotation=45)

                # Criar uma instância de FigureCanvasQTAgg
                canvas = FigureCanvas(fig)

                # Verificar se a graphicsView tem um layout
                if self.ui.graphicsView.layout() is None:
                    # Se não houver layout, adicionar um QVBoxLayout
                    layout = QtWidgets.QVBoxLayout(self.ui.graphicsView)
                    layout.setContentsMargins(0, 0, 0, 0)
                    layout.addWidget(canvas)
                else:
                    # Se já houver um layout, substituir o widget existente
                    old_widget = self.ui.graphicsView.layout().itemAt(0).widget()
                    self.ui.graphicsView.layout().replaceWidget(old_widget, canvas)
                    old_widget.close()

                canvas.draw()

        except Exception as e:
            # Tratar exceções gerais
            print(f"Erro: {e}")

    def verificar_tabela_existente(self, cursor, data_ex):
        # Verificar se a tabela existe no banco de dados
        try:
            cursor.execute(f"SHOW TABLES LIKE 'tabela_{data_ex}'")
            return cursor.fetchone() is not None
        except mysql.connector.Error as err:
            # Handle the error
            print(f"Error: {err}")
            return False

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

                    print(simbolos_encontrados)
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
                        numero_float = float(string_numerica)

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
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
