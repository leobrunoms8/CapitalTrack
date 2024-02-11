from PyQt5.QtWidgets import QApplication, QMainWindow

from Rotinas.FrontEnd.Interface.Window_Main import Ui_MainWindow
from Rotinas.Window_Exibir_Dividendos import Window_exibir_Dividendos
from Rotinas.Window_Exibir_Listas import Window_exibir_listas
from Rotinas.Window_Exibir_Graficos import Window_exibir_Graficos
from Rotinas.Window_Exibir_Analises import Window_exibir_Analises
from Rotinas.Window_Exibir_Ordens import Window_exibir_ordens
from Rotinas.Window_Exibir_Modos import Window_exibir_modos
from Rotinas.Metodos.Processamento_de_Imagens import Leitura_de_Ordem


import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create an instance of the main window design class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Dados a serem repassados as classes seguintes
        host = "localhost"
        user = "developer"
        password = "Leo140707"
        database = "RaspagemPuraDeDados"
        

        # Connect menu item signals to corresponding functions
        self.ui.actionListas.triggered.connect(self.exibir_listas)
        self.ui.actionDividendos.triggered.connect(self.exibir_dividendos)
        self.ui.actionGr_ficos.triggered.connect(self.exibir_graficos)
        self.ui.actionAnalises.triggered.connect(self.exibir_analises)
        self.ui.actionLer_Ordem.triggered.connect(self.executar_leitura_ordem)
        self.ui.actionOrdens.triggered.connect(self.exibir_ordens)
        self.ui.actionModos.triggered.connect(self.exibir_modos)

        # Mantenha uma instância da classe Window_exibir_Dividendos como um atributo
        self.dividendos_window_instance = Window_exibir_Dividendos(self.ui, host, user, password, database)
        self.exibir_listas_instance = Window_exibir_listas(self.ui, host, user, password, database)
        self.exibir_graficos_instance = Window_exibir_Graficos(self.ui)
        self.exbir_ordens_instance = Window_exibir_ordens(self.ui)
        self.exibir_analises_instance = Window_exibir_Analises(self.ui, host, user, password, database)
        self.exbir_modos_instance = Window_exibir_modos(self)

    def exibir_listas(self):
       # Chamar o método exibir_listas na instância da classe
       self.exibir_listas_instance.exibir_listas()

    def exibir_dividendos(self):
        # Chamar o método exibir_dividendos na instância da classe
        self.dividendos_window_instance.exibir_dividendos()
    
    def exibir_graficos(self):
        self.exibir_graficos_instance.exibir_grafico()
    
    def exibir_analises(self):
        self.exibir_analises_instance.exibir_analises()
    
    def exibir_ordens(self):
        self.exbir_ordens_instance.exibir_ordens()

    def executar_leitura_ordem(self):
        self.ler_ordem_instance = Leitura_de_Ordem()
        self.ler_ordem_instance.ler_ordem()
    
    def exibir_modos(self):
        self.exbir_modos_instance.exibir_modos()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
 