import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QDateTime

class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Execução de Métodos Fictícios")
        self.resize(400, 150)

        layout = QVBoxLayout()

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)

        # Horários para execução dos métodos fictícios
        self.horarios_execucao = [
            "09:00:00",  # Método 1
            "12:30:00",  # Método 2
            "18:15:00"   # Método 3
        ]

        # Inicializa o timer para atualizar a data e hora a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_data_hora)
        self.timer.start(1000)  # a cada 1000 ms (1 segundo)

        # Atualiza a data e hora assim que a janela for mostrada
        self.atualizar_data_hora()

    def atualizar_data_hora(self):
        # Obtém a data e hora atual
        data_hora_atual = QDateTime.currentDateTime()
        # Formata a data e hora como string
        data_hora_formatada = data_hora_atual.toString("dd/MM/yyyy HH:mm:ss")
        # Define a string formatada como texto da label
        self.label.setText(data_hora_formatada)

        # Verifica se é hora de executar os métodos fictícios
        hora_atual = data_hora_atual.toString("HH:mm:ss")
        if hora_atual in self.horarios_execucao:
            # Chama o método correspondente ao horário atual
            indice = self.horarios_execucao.index(hora_atual) + 1
            metodo = getattr(self, f"metodo_{indice}", None)
            if metodo:
                metodo()

    # Métodos fictícios a serem executados em horários específicos
    def metodo_1(self):
        print("Método 1 foi acionado às 09:00:00")

    def metodo_2(self):
        print("Método 2 foi acionado às 12:30:00")

    def metodo_3(self):
        print("Método 3 foi acionado às 18:15:00")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
