import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from FrontEnd.Interface.Window_Main import Ui_MainWindow
from FrontEnd.Interface.Window_Listas import Ui_Listas
from FrontEnd.Interface.Window_Dividendos import Ui_Dividendos
from Investing.RasparDados import RaspagemInvesting
import mysql.connector


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Crie uma instância da classe de design gerada
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conecte os sinais dos itens de menu às funções correspondentes
        self.ui.actionTela_Cheia.triggered.connect(self.exibir_tela_cheia)
        self.ui.actionListas.triggered.connect(self.exibir_listas)
        self.ui.actionDividendos.triggered.connect(self.exibir_dividendos)

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

        self.ui.dividendos_window.show()

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
