import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import mimetypes
import cv2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.setWindowTitle("Exibir Arquivos")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Botão para listar arquivos
        self.btn_listar = QPushButton("Listar Arquivos")
        self.btn_listar.clicked.connect(self.listar_arquivos)
        layout.addWidget(self.btn_listar)

        # Tabela para exibir nomes e extensões dos arquivos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Extensão"])
        layout.addWidget(self.table_widget)

        # Conectar o sinal itemClicked à função exibir_imagem
        self.table_widget.itemClicked.connect(self.exibir_imagem)

        # Label para exibir a imagem
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # Label para exibir o texto extraído
        self.text_label = QLabel()
        layout.addWidget(self.text_label)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def listar_arquivos(self):
        # Pasta a ser verificada
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack"  # Altere para o caminho da sua pasta

        # Limpar tabela
        self.table_widget.setRowCount(0)

        # Listar arquivos na pasta
        arquivos = os.listdir(pasta)

        # Adicionar arquivos à tabela
        for arquivo in arquivos:
            # Ignorar pastas e arquivos ocultos
            if os.path.isfile(os.path.join(pasta, arquivo)) and not arquivo.startswith('.'):
                nome, extensao = os.path.splitext(arquivo)
                tipo_mime, _ = mimetypes.guess_type(arquivo)
                if tipo_mime and tipo_mime.startswith('image'):
                    row_position = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_position)
                    self.table_widget.setItem(row_position, 0, QTableWidgetItem(nome))
                    self.table_widget.setItem(row_position, 1, QTableWidgetItem(extensao))

    def exibir_imagem(self, item):
        # Pasta onde estão as imagens
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack"  # Altere para o caminho da sua pasta

        # Obtém o nome da imagem selecionada
        nome_imagem = item.text()

        # Carrega a imagem na QLabel
        caminho_imagem = os.path.join(pasta, nome_imagem)
        pixmap = QPixmap(caminho_imagem)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Extrai texto da imagem
        texto_extraido = self.extract_text_from_image(caminho_imagem)
        self.text_label.setText(texto_extraido)

    def extract_text_from_image(self, image_path):
        # Carregar imagem
        image = cv2.imread(image_path)

        # Segmentar regiões de texto
        text_regions = self.segment_text_regions(image)

        # Reconhecer texto em cada região
        extracted_text = ""
        for region in text_regions:
            # Aqui você pode usar alguma biblioteca de reconhecimento de texto, como Tesseract OCR
            # Para este exemplo, vamos apenas converter a região para texto preto e branco
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            text = self.ocr_processing(binary)
            extracted_text += text + "\n"  # Adiciona uma nova linha entre as regiões de texto

        return extracted_text

    def segment_text_regions(self, image):
        # Convertendo a imagem para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicando suavização para remover ruídos
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Aplicando binarização para destacar o texto
        _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

        # Encontrando contornos na imagem binária
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Criando uma lista para armazenar as regiões de texto segmentadas
        text_regions = []

        # Iterando sobre os contornos encontrados
        for contour in contours:
            # Obtendo o retângulo delimitador do contorno
            x, y, w, h = cv2.boundingRect(contour)

            # Adicionando a região de texto delimitada pelo retângulo à lista
            text_regions.append(image[y:y+h, x:x+w])

        return text_regions

    def ocr_processing(self, image):
        # Aqui você pode usar uma biblioteca de OCR, como Tesseract OCR
        # Este é apenas um exemplo de processamento básico para simular o reconhecimento de texto
        return "Texto Extraído"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
