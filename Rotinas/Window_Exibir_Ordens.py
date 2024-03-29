from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .FrontEnd.Interface.Window_Ordens import Ui_Window_Ordens
from .Metodos.Processamento_de_Imagens import Leitura_de_Ordem
from .Metodos.Pesquisar_em_Tabelas import PesquisarEmTabelas
from .Metodos.Atualizar_Tabelas import Atualizar_Tabelas

import os
import mimetypes
import mysql.connector

class Window_exibir_ordens(QDialog):
    def __init__(self, ui_mainwindow, host, user, password, database):
        super(Window_exibir_ordens, self).__init__()

        # Recebe a instância da classe Ui_MainWindow
        self.ui_mainwindow = ui_mainwindow
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        # Crie uma instância da classe Ui_Window_Ordens
        self.ui_ordens = Ui_Window_Ordens()
        self.ui_ordens.setupUi(self)

        # Conecte o clique do botão à função que executa o código desejado
        self.ui_ordens.pushButton.clicked.connect(self.verificar_notas_recebidas)
        self.ui_ordens.pushButton_2.clicked.connect(self.iniciar_trade)
        self.ui_ordens.pushButton_3.clicked.connect(self.inserir_trade_na_lista)
        self.ui_ordens.pushButton_4.clicked.connect(self.listar_todos_os_trades)
        self.ui_ordens.pushButton_5.clicked.connect(self.calculo_finalizacao_trade)
        self.ui_ordens.pushButton_7.clicked.connect(self.finalizar_trade)

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

    def iniciar_trade(self):
        # Atribui valor depositado em LineEdit na variável simbolo
        simbolo =  self.ui_ordens.lineEdit.text()

        # Inicia a verificação em banco de dados
        # Nome da Empresa
        pesquisa = PesquisarEmTabelas(self.host, self.user, self.password, self.database)
        nome_da_empresa = pesquisa.nome_da_empresa_com_simbolo(simbolo)
        self.ui_ordens.label_9.setText(nome_da_empresa)
        # Moeda
        moeda = pesquisa.moeda_com_simbolo(simbolo)
        self.ui_ordens.label_10.setText(moeda)
        # Frequencia
        frequencia = pesquisa.frequencia_com_simbolo(simbolo)
        self.ui_ordens.label_12.setText(frequencia)
        # Proximo Dividendo
        prox_dividendo = pesquisa.proximo_dividendo_com_simbolo(simbolo)
        self.ui_ordens.label_14.setText(prox_dividendo)
        # Valor do Dividendo
        valor_dividendo = pesquisa.valor_dividendo_com_simbolo(simbolo)
        self.ui_ordens.label_16.setText(valor_dividendo)

    def inserir_trade_na_lista(self):
        # Atribui valores depositados em LineEdits nas variáveis
        simbolo =  self.ui_ordens.lineEdit.text()
        valor_de_entrada = float(self.ui_ordens.lineEdit_2.text())
        quantidade = int(self.ui_ordens.lineEdit_3.text())
        data_de_entrada = self.ui_ordens.lineEdit_4.text()
        dividendo = float(self.ui_ordens.lineEdit_5.text())
        premio = float(self.ui_ordens.lineEdit_6.text())
        data_ex = self.ui_ordens.lineEdit_7.text()
        data_pagamento = self.ui_ordens.lineEdit_8.text()
        corretora = self.ui_ordens.lineEdit_9.text()
        moeda = self.ui_ordens.lineEdit_10.text()

        atualizador = Atualizar_Tabelas(self.host, self.user, self.password, self.database)
        id_inserido = atualizador.atualizar_tabela_trade(simbolo, valor_de_entrada, quantidade, data_de_entrada, dividendo, premio, data_ex, data_pagamento, corretora, moeda)
        print(id_inserido)

    def calculo_finalizacao_trade(self):
        # Atribui valores depositados em LineEdits nas variáveis 
        id =  int(self.ui_ordens.lineEdit_18.text())
        valor_de_saida = float(self.ui_ordens.lineEdit_17.text())
        quantidade_de_saida = int(self.ui_ordens.lineEdit_16.text())
        

        # Inicia a verificação em banco de dados
        pesquisa = PesquisarEmTabelas(self.host, self.user, self.password, self.database)

        trade = pesquisa.trade_com_id(id)
        # Verifica se há resultados da consulta
        if trade: 
            # Atribui valor de entrada para cálculos de ganho
            valor_de_entrada = float(trade[0])
            # Atribui valor de quantidade para finalização de Trade  
            quantidade_de_entrada = int(trade[1]) 
            if quantidade_de_saida == quantidade_de_entrada:
                print('Trade Finalizado')
            else:
                print('Trade não Finalizado')
            
            # Cálculo de Ganho Real
            valor_investido = quantidade_de_entrada * valor_de_entrada
            valor_liquidado = quantidade_de_saida * valor_de_saida
            self.ganho_real = valor_liquidado - valor_investido

            # Cálculo de Ganho Percentual
            self.ganho_percentual = (self.ganho_real / valor_investido) * 100
        else:
            print(f"Trade com ID {id} não encontrado.")
        
        # Verifica se foi acerto ou Ganho
        if self.ganho_real >= 0:
            self.acerto = 'S'
        else:
            self.acerto = 'N'
            
        
        self.ui_ordens.label_33.setText(str(self.ganho_real))
        self.ui_ordens.label_24.setText(str(self.ganho_percentual) + '%')
        self.ui_ordens.label_22.setText(self.acerto)
    
    def finalizar_trade(self):
        # Atribui valores depositados em LineEdits nas variáveis 
        id =  int(self.ui_ordens.lineEdit_18.text())
        valor_de_saida = float(self.ui_ordens.lineEdit_17.text())
        quantidade_de_saida = int(self.ui_ordens.lineEdit_16.text())
        data_de_saida = self.ui_ordens.lineEdit_15.text()
        link_para_trade = id

        atualizador = Atualizar_Tabelas(self.host, self.user, self.password, self.database)
        atualizador.finalizar_tabela_trade(id, valor_de_saida, quantidade_de_saida, data_de_saida, self.ganho_real, self.ganho_percentual, self.acerto, link_para_trade)

    def listar_todos_os_trades(self):
        # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM lista_de_trades")

            # Recupere os resultados
            result = cursor.fetchall()

            # Commit da transação
            db.commit()

            # Fechar cursor e conexão
            cursor.close()
            db.close()

        # Preencha a tabela na janela de "Dividendos"
            self.ui_ordens.tableWidget_2.setRowCount(len(result))
            for row_index, row_data in enumerate(result):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui_ordens.tableWidget_2.setItem(row_index, col_index, item)

