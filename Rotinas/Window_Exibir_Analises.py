from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidgetItem, QMessageBox
from forex_python.converter import CurrencyRates
from datetime import datetime, timedelta
import yfinance as yf
import mysql.connector

from .FrontEnd.Interface.Window_Analises import Ui_Analises
from .Metodos.Testagem_Yfinance_por_data import Testagem_Yfinance
from .Metodos.Apagar_Tabela_Generico import ApagarTabelaGenerico
from .Metodos.Criar_Tabela_Generico import CriarTabelaGenerico

class Window_exibir_Analises(QDialog):
    def __init__(self, ui_mainwindow):
        super(Window_exibir_Analises, self).__init__()

        # Recebe a instância da classe Ui_MainWindow
        self.ui_mainwindow = ui_mainwindow

        # Crie uma instância da classe ui_analises
        self.ui_analises = Ui_Analises()
        self.ui_analises.setupUi(self)

    def exibir_analises(self):

        # Conecte o clique do botão à função que executa o código desejado
        self.ui_analises.pushButton.clicked.connect(self.analisar_por_data)
        self.ui_analises.pushButton_2.clicked.connect(self.analisar_por_acao)
        
        self.show()
    def analisar_por_data(self):
            # Verifique se hoje é sábado ou domingo
            data_ex = self.ui_analises.dateEdit.date().toString("dd.MM.yyyy")
            data_formato = "%d.%m.%Y"
            data_objeto = datetime.strptime(data_ex, data_formato)
            dia_semana = data_objeto.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

            if dia_semana == 5 or dia_semana == 6:  # 5 é sábado, 6 é domingo
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
            
            # Define o dia de hoje
            tabela_nome = f"`tabela_{data_ex}`"

            # Método para coletar dados da tabela de dividendos do dia

            self.testagem = Testagem_Yfinance()
            simbolos_encontrados = self.testagem.testagem_por_data_encontrados(data_ex)
            #simbolos_nao_encontrados = self.testagem.testagem_por_data_nao_encontrados(data_ex)

            print('Símbolos Encontrados')
            print(simbolos_encontrados)


            # -------------- Dropar tabela racunho ----------
            
            self.drop = ApagarTabelaGenerico()
            self.drop.apagar_tabela_generico('rascunho')

            # -------------- Criar tabela rascunho --------------
            
            # Comando SQL para criar a tabela com as colunas desejadas
            criar_tabela_sql = """
            CREATE TABLE IF NOT EXISTS rascunho (
                simbolo VARCHAR(255) NOT NULL,
                nome_da_empresa VARCHAR(255) NOT NULL,
                data_ex DATE NOT NULL,
                moeda VARCHAR(255) NOT NULL,
                valor_dividendo DECIMAL(7, 6) NOT NULL,
                valor_em_BRL DECIMAL(7, 6) NOT NULL,
                frequencia VARCHAR(50) NOT NULL,
                data_pagamento DATE NOT NULL,
                percentual_acao DECIMAL(7, 6) NOT NULL
            )
            """   
            self.criacao = CriarTabelaGenerico()
            self.criacao.criar_tabela_generico(criar_tabela_sql)     

            # -----------------   Pegar linha a linha de acordo com a lista de encontrados -------------

            # Análise de preço da ação encontrada

            for simbolo in simbolos_encontrados:

                valor_da_acao = self.testagem.testagem_preco(simbolo)
                print(valor_da_acao)
            
            # Análise frequancia de dividendos da empresa
            
            for simbolo in simbolos_encontrados:

                frequencia_da_acao = self.testagem.testagem_frequencia_de_dividendos(simbolo)
                print(frequencia_da_acao)

            # Análise de moeda da ação
                
            for simbolo in simbolos_encontrados:

                moeda = self.testagem.testagem_moeda_da_acao(simbolo)
                print(moeda)




                
    def analisar_por_acao(self):
       pass

               
    def switch_case_numero_dia_da_semana0(self, argument):
        switch_dict = {
            0: 7,
            1: 6,
            2: 5,
            3: 4,
            4: 3,
            5: 2,
            6: 1,
        }

        return switch_dict.get(argument, 'Esta é a execução padrão')

    def switch_case_numero_dia_da_semana1(self, argument):
        switch_dict = {
            0: 14,
            1: 13,
            2: 12,
            3: 11,
            4: 10,
            5: 9,
            6: 8,
        }
    
        return switch_dict.get(argument, 'Esta é a execução padrão')
    
    def switch_case_numero_dia_da_semana2(self, argument):
        switch_dict = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
        }

        return switch_dict.get(argument, 'Esta é a execução padrão')
