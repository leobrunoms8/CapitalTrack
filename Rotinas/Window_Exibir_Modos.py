from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer, QDateTime
from .FrontEnd.Interface.Window_Modos import Ui_Modos
from .Metodos.Gerenciar_Modo_Automatico import Gerenciador_Modo_Automatico

class Window_exibir_modos(QDialog):
    def __init__(self, ui_mainwindow, host, user, password, database):
        super(Window_exibir_modos, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        # Posição de seletora de Modo Manual/Automático
        self.modo = 'manual'

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
        self.ui_modos.pushButton.clicked.connect(self.set_modo_auto)
        self.ui_modos.pushButton_2.clicked.connect(self.set_modo_manual)
        print (self.modo)


        # Instância do gerenciador de modo automático
        self.gerenciador = Gerenciador_Modo_Automatico(self.host, self.user, self.password, self.database)

    def exibir_modos(self):
        self.show()
    
    def atualizar_data_hora(self):
        # Obtém a data e hora atual
        self.data_hora_atual = QDateTime.currentDateTime()
        # Formata a data e hora como string
        data_hora_formatada = self.data_hora_atual.toString("dd/MM/yyyy HH:mm:ss")
        # Define a string formatada como texto da label
        self.ui_modos.label_4.setText(data_hora_formatada)

        # Verifica estado da seletora
        if self.modo == 'auto':
            self.modo_automatico()
        if self.modo == 'manual':
            self.modo_manual()

    def modo_automatico(self):
        hora_formatada = self.data_hora_atual.toString("HH:mm:ss")
        self.ui_modos.label_2.setText('Modo Automático')
        texto = self.gerenciador.atualizar_data_hora(hora_formatada)
        self.ui_modos.label_6.setText(texto)
    
    def modo_manual(self):
        self.ui_modos.label_2.setText('Modo Manual')
        self.ui_modos.label_6.setText('Aguardando Modo Auto')

    def set_modo_auto(self):
        self.modo = 'auto'
    
    def set_modo_manual(self):
        self.modo = 'manual'

    