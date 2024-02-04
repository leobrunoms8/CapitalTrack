import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        self.setGeometry(100, 100, 300, 150)

        self.button = QPushButton("Mostrar Hello World", self)
        self.button.setGeometry(50, 50, 200, 30)
        self.button.clicked.connect(self.show_hello_world)

        self.label = QLabel("", self)
        self.label.setGeometry(50, 90, 200, 30)

    def show_hello_world(self):
        self.label.setText("Hello World")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
