from PyQt5.QtWidgets import QApplication, QMainWindow

from Rotinas.FrontEnd.Interface.Window_Main import Ui_MainWindow
from Rotinas.Window_Exibir_Dividendos import Window_exibir_Dividendos
from Rotinas.Window_Exibir_Listas import Window_exibir_listas
from Rotinas.Window_Exibir_Graficos import Window_exibir_Graficos


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
        self.ui.actionGr_ficos.triggered.connect(self.exibir_graficos)

        # Mantenha uma instância da classe Window_exibir_Dividendos como um atributo
        self.dividendos_window_instance = Window_exibir_Dividendos(self.ui)
        self.exibir_listas_instance = Window_exibir_listas(self.ui)
        self.exibir_graficos_instance = Window_exibir_Graficos(self.ui)

        

    def exibir_listas(self):
       # Chamar o método exibir_listas na instância da classe
       self.exibir_listas_instance.exibir_listas()

    def exibir_tela_cheia(self):
        # Implemente a lógica para exibir a tela cheia aqui
        pass

    def exibir_dividendos(self):
        # Chamar o método exibir_dividendos na instância da classe
        self.dividendos_window_instance.exibir_dividendos()
    
    def exibir_graficos(self):
        self.exibir_graficos_instance.exibir_grafico()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
