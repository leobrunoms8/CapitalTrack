import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QDateTime

class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data e Hora em Tempo Real")
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
