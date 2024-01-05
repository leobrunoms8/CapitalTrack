from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidgetItem
from Rotinas.FrontEnd.Interface.Window_Listas import Ui_Listas
from Investing.RasparDados import RaspagemInvesting

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
            # Conecte o clique do botão à função que executa o código desejado
            self.ui_listas.pushButton_2.clicked.connect(self.executar_raspagem)

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


            

    def executar_raspagem(self):
        # Executar ao clicar no pushButton_2
        url = "https://br.investing.com/dividends-calendar/"
        raspagem = RaspagemInvesting(url)
        raspagem.realizar_raspagem()