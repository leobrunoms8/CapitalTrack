from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidgetItem, QMessageBox
from datetime import datetime

from Rotinas.FrontEnd.Interface.Window_Listas import Ui_Listas
from Rotinas.Metodos.Raspagem_e_Separacao import Raspagem_e_Separacao_Investing

import mysql.connector

class Window_exibir_listas(QDialog):
    def __init__(self, ui_mainwindow):
        super(Window_exibir_listas, self).__init__()

        # Recebe a instância da classe Ui_MainWindow
        self.ui_mainwindow = ui_mainwindow

        # Crie uma instância da classe Ui_Dividendos
        self.ui_listas = Ui_Listas()
        self.ui_listas.setupUi(self)

    def exibir_listas(self):
        self.show()
        # Conecte o clique do botão à função que executa o código desejado -- Raspagens
        self.ui_listas.pushButton.clicked.connect(self.executar_raspagem_hoje)
        self.ui_listas.pushButton_2.clicked.connect(self.executar_raspagem_proxima_semana)
        self.ui_listas.pushButton_3.clicked.connect(self.executar_raspagem_essa_semana)
        self.ui_listas.pushButton_4.clicked.connect(self.executar_raspagem_amanha)

        # Conecte o clique do botão à função que executa o código desejado -- Análises

        # Conecte o clique do botão à função que executa o código desejado -- Verificações

                
    def executar_raspagem_hoje(self):
        # Verifique se hoje é sábado ou domingo
        hoje = datetime.now()
        dia_semana = hoje.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

        if dia_semana == 5 or dia_semana == 6:  # 4 é sexta, 5 é sábado
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
        
        raspagem = Raspagem_e_Separacao_Investing("timeFrame_today")
        raspagem.realizar_raspagem()

        self.preencher_tablela()

    def executar_raspagem_amanha(self):
        # Verifique se hoje é sexta ou sábado
        hoje = datetime.now()
        dia_semana = hoje.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

        if dia_semana == 4 or dia_semana == 5:  # 4 é sexta, 5 é sábado
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Amanhã é fim de semana. Não há consulta de dividendos disponível.")
                return

        raspagem = Raspagem_e_Separacao_Investing("timeFrame_tomorrow")
        raspagem.realizar_raspagem()

        self.preencher_tablela()

    def executar_raspagem_essa_semana(self):
        raspagem = Raspagem_e_Separacao_Investing("timeFrame_thisWeek")
        raspagem.realizar_raspagem()

        self.preencher_tablela()

    def executar_raspagem_proxima_semana(self):
        raspagem = Raspagem_e_Separacao_Investing("timeFrame_nextWeek")
        raspagem.realizar_raspagem()

        self.preencher_tablela()
    
    def preencher_tablela(self):
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