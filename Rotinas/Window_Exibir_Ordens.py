from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .FrontEnd.Interface.Window_Ordens import Ui_Window_Ordens
from .Metodos.Processamento_de_Imagens import Leitura_de_Ordem

import os
import mimetypes

class Window_exibir_ordens(QDialog):
    def __init__(self, ui_mainwindow):
        super(Window_exibir_ordens, self).__init__()

        # Recebe a instância da classe Ui_MainWindow
        self.ui_mainwindow = ui_mainwindow

        # Crie uma instância da classe Ui_Window_Ordens
        self.ui_ordens = Ui_Window_Ordens()
        self.ui_ordens.setupUi(self)

        # Conecte o clique do botão à função que executa o código desejado
        self.ui_ordens.pushButton.clicked.connect(self.verificar_notas_recebidas)

    def exibir_ordens(self):
        self.show()

    def verificar_notas_recebidas(self):
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack\Rotinas\Metodos\Imagens"

        # Executa a verificação de notas recebidas
        self.listar_arquivos(pasta)

        # Conectar o sinal itemClicked à função exibir_imagem
        self.ui_ordens.tableWidget.itemClicked.connect(self.exibir_imagem)

        #r'C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack\Rotinas\Metodos\Imagens\Nota_2024_02_01_Edited.jpg'

    def listar_arquivos(self, pasta_destino):
        pasta = pasta_destino
        self.ui_ordens.tableWidget.setRowCount(0)  # Limpa a tabela antes de preencher
        arquivos = os.listdir(pasta)
        print(arquivos)

        for arquivo in arquivos:
            if os.path.isfile(os.path.join(pasta, arquivo)) and not arquivo.startswith('.'):
                nome, extensao = os.path.splitext(arquivo)
                tipo_mime, _ = mimetypes.guess_type(arquivo)
                if tipo_mime and tipo_mime.startswith('image'):
                    row_position = self.ui_ordens.tableWidget.rowCount()
                    self.ui_ordens.tableWidget.insertRow(row_position)
                    self.ui_ordens.tableWidget.setItem(row_position, 0, QTableWidgetItem(nome))
                    self.ui_ordens.tableWidget.setItem(row_position, 1, QTableWidgetItem(extensao))
    
    def exibir_imagem(self, item):
        pasta = r"C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack\Rotinas\Metodos\Imagens"
        nome_imagem = item.text()
        caminho_imagem = os.path.join(pasta, nome_imagem)
        pixmap = QPixmap(caminho_imagem)
        self.ui_ordens.label_2.setPixmap(pixmap)
        self.ui_ordens.label_2.setAlignment(Qt.AlignCenter)

        # Obter o caminho completo do arquivo selecionado na tabela
        nome_imagem_para_extracao = nome_imagem + '.jpg'
        print(nome_imagem_para_extracao)
        item_para_extracao = os.path.join(pasta, nome_imagem_para_extracao)

        texto_extraido = self.extract_text_from_image(item_para_extracao)
        print(texto_extraido)
        self.ui_ordens.label.setText(texto_extraido)
        self.caregamento_de_informacoes_da_nota(texto_extraido)


    def extract_text_from_image(self, image_path):
        self.leitura = Leitura_de_Ordem()
        texto_da_imagem = self.leitura.ler_ordem_automatico(image_path)
        return texto_da_imagem
    
    def caregamento_de_informacoes_da_nota(self, texto):
        linhas = texto.split('\n')

        # Procurar as informações relevantes nas linhas extraídas
        informacoes = {
            'codigo': None,
            'quantidade_solicitada': None,
            'quantidade_executada': None,
            'preco_medio': None
        }

        for linha in linhas:
            if 'HGRUMN' in linha:
                informacoes['codigo'] = linha.strip()
            elif 'Quantidade solicitada' in linha:
                informacoes['quantidade_solicitada'] = int(linha.split()[-1])
            elif 'Quantidade executada' in linha:
                informacoes['quantidade_executada'] = int(linha.split()[-1])
            elif 'Preço médio' in linha:
                informacoes['preco_medio'] = float(linha.split()[-1].replace('R$', '').replace(',','.').strip())

        # Imprimir as informações no terminal
        print("Código:", informacoes['codigo'])
        print("Quantidade solicitada:", informacoes['quantidade_solicitada'])
        print("Quantidade executada:", informacoes['quantidade_executada'])
        print("Preço médio:", informacoes['preco_medio'])

        

                



