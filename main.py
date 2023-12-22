import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from FrontEnd.Interface.Window_Main import Ui_MainWindow
from FrontEnd.Interface.Window_Listas import Ui_Listas
from FrontEnd.Interface.Window_Dividendos import Ui_Dividendos
from Investing.RasparDados import RaspagemInvesting
from datetime import datetime, timedelta
import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql


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
                ax.set_xlabel('Data de Pagamento')
                ax.set_ylabel('Soma do Valor de Dividendo')
                ax.set_title('Soma do Valor de Dividendo por Data de Pagamento')
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
