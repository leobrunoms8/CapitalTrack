from PyQt5.QtWidgets import QDialog
from .FrontEnd.Interface.Window_Calendario import Ui_Calendario

class Window_exibir_calendario(QDialog):
    def __init__(self, ui_mainwindow, host, user, password, database):
        super(Window_exibir_calendario, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        # Posição de seletora de Modo Manual/Automático
        self.modo = 'manual'

        # Recebe a instância da classe Ui_MainWindow
        self.ui_calendario = ui_mainwindow

        # Crie uma instância da classe Ui_Window_Modos
        self.ui_calendario = Ui_Calendario()
        self.ui_calendario.setupUi(self)

    def exibir_calendario(self):
        self.show()