import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import mimetypes
import cv2

class Verificacao_Notas_Recebidas(QMainWindow):
    def __init__(self, ui_mainwindow=None):
        super(Verificacao_Notas_Recebidas, self).__init__()
        if ui_mainwindow:
            self.ui_mainwindow = ui_mainwindow
            self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Exibir Arquivos")
        self.setGeometry(100, 100, 800, 600)
        self.create_layout()
        self.create_widgets()
        self.connect_signals()

    def create_layout(self):
        self.layout = QVBoxLayout()

    def create_widgets(self):
        self.btn_listar = QPushButton("Listar Arquivos")
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Extensão"])
        self.image_label = QLabel()
        self.text_label = QLabel()

        self.layout.addWidget(self.btn_listar)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.text_label)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def connect_signals(self):
        self.btn_listar.clicked.connect(self.listar_arquivos)
        self.table_widget.itemClicked.connect(self.exibir_imagem)

    def listar_arquivos(self):
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack"
        self.table_widget.setRowCount(0)
        arquivos = os.listdir(pasta)

        for arquivo in arquivos:
            if os.path.isfile(os.path.join(pasta, arquivo)) and not arquivo.startswith('.'):
                nome, extensao = os.path.splitext(arquivo)
                tipo_mime, _ = mimetypes.guess_type(arquivo)
                if tipo_mime and tipo_mime.startswith('image'):
                    row_position = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_position)
                    self.table_widget.setItem(row_position, 0, QTableWidgetItem(nome))
                    self.table_widget.setItem(row_position, 1, QTableWidgetItem(extensao))

    def exibir_imagem(self, item):
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack"
        nome_imagem = item.text()
        caminho_imagem = os.path.join(pasta, nome_imagem)
        pixmap = QPixmap(caminho_imagem)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        texto_extraido = self.extract_text_from_image(caminho_imagem)
        self.text_label.setText(texto_extraido)

    def extract_text_from_image(self, image_path):
        image = cv2.imread(image_path)
        text_regions = self.segment_text_regions(image)
        extracted_text = ""
        for region in text_regions:
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            text = self.ocr_processing(binary)
            extracted_text += text + "\n"
        return extracted_text

    def segment_text_regions(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            text_regions.append(image[y:y+h, x:x+w])
        return text_regions

    def ocr_processing(self, image):
        return "Texto Extraído"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Verificacao_Notas_Recebidas()
    window.show()
    sys.exit(app.exec_())

    #----------------------------------- Cógigo antigo -------------------------------
            def create_layout(self):
        self.layout = QVBoxLayout()

    def create_widgets(self):
        self.btn_listar = QPushButton("Listar Arquivos")
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Extensão"])
        self.image_label = QLabel()
        self.text_label = QLabel()

        self.layout.addWidget(self.btn_listar)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.text_label)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def connect_signals(self):
        self.btn_listar.clicked.connect(self.listar_arquivos)
        self.table_widget.itemClicked.connect(self.exibir_imagem)

    def listar_arquivos(self):
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack"
        self.table_widget.setRowCount(0)
        arquivos = os.listdir(pasta)

        for arquivo in arquivos:
            if os.path.isfile(os.path.join(pasta, arquivo)) and not arquivo.startswith('.'):
                nome, extensao = os.path.splitext(arquivo)
                tipo_mime, _ = mimetypes.guess_type(arquivo)
                if tipo_mime and tipo_mime.startswith('image'):
                    row_position = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_position)
                    self.table_widget.setItem(row_position, 0, QTableWidgetItem(nome))
                    self.table_widget.setItem(row_position, 1, QTableWidgetItem(extensao))

    def exibir_imagem(self, item):
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack"
        nome_imagem = item.text()
        caminho_imagem = os.path.join(pasta, nome_imagem)
        pixmap = QPixmap(caminho_imagem)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        texto_extraido = self.extract_text_from_image(caminho_imagem)
        self.text_label.setText(texto_extraido)

    def extract_text_from_image(self, image_path):
        image = cv2.imread(image_path)
        text_regions = self.segment_text_regions(image)
        extracted_text = ""
        for region in text_regions:
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            text = self.ocr_processing(binary)
            extracted_text += text + "\n"
        return extracted_text

    def segment_text_regions(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            text_regions.append(image[y:y+h, x:x+w])
        return text_regions

    def ocr_processing(self, image):
        return "Texto Extraído"


