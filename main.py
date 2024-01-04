from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from Rotinas.FrontEnd.Interface.Window_Main import Ui_MainWindow
from Rotinas.FrontEnd.Interface.Window_Listas import Ui_Listas
from Rotinas.Window_Exibir_Dividendos import Window_exibir_Dividendos
from Investing.RasparDados import RaspagemInvesting
from datetime import datetime
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
        self.ui.pushButton.clicked.connect(self.exibir_grafico) 

        # Mantenha uma instância da classe Window_exibir_Dividendos como um atributo
        self.dividendos_window_instance = Window_exibir_Dividendos(self.ui)

        

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
        # Chame o método exibir_dividendos na instância da classe
        self.dividendos_window_instance.exibir_dividendos()

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
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
