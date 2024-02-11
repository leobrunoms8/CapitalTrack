from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer, QDateTime
from .FrontEnd.Interface.Window_Modos import Ui_Modos

class Window_exibir_modos(QDialog):
    def __init__(self, ui_mainwindow):
        super(Window_exibir_modos, self).__init__()

        # Recebe a instância da classe Ui_MainWindow
        self.ui_mainwindow = ui_mainwindow

        # Crie uma instância da classe Ui_Window_Modos
        self.ui_modos = Ui_Modos()
        self.ui_modos.setupUi(self)

        # Inicializa o timer para atualizar a data e hora a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_data_hora)
        self.timer.start(1000)  # a cada 1000 ms (1 segundo)

        # Atualiza a data e hora assim que a janela for mostrada
        self.atualizar_data_hora()

        # Conecte o clique do botão à função que executa o código desejado
        self.ui_modos.pushButton.clicked.connect(self.modo_automatico)

    def exibir_modos(self):
        self.show()
    
    def atualizar_data_hora(self):
        # Obtém a data e hora atual
        data_hora_atual = QDateTime.currentDateTime()
        # Formata a data e hora como string
        data_hora_formatada = data_hora_atual.toString("dd/MM/yyyy HH:mm:ss")
        # Define a string formatada como texto da label
        self.ui_modos.label_4.setText(data_hora_formatada)

    def modo_automatico(self):
        self.ui_modos.label_6.setText('Modo Automático')


    