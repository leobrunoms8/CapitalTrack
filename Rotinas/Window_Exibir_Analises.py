from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from datetime import datetime, timedelta
import mysql.connector

from .FrontEnd.Interface.Window_Analises import Ui_Analises
from .Metodos.Testagem_Yfinance_por_data import Testagem_Yfinance
from .Metodos.Apagar_Tabela_Generico import ApagarTabelaGenerico
from .Metodos.Criar_Tabela_Generico import CriarTabelaGenerico
from .Metodos.Atualizar_Tabelas import Atualizar_Tabelas

class Window_exibir_Analises(QDialog):
    def __init__(self, ui_mainwindow, host, user, password, database):
        super(Window_exibir_Analises, self).__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        # Recebe a instância da classe Ui_MainWindow
        self.ui_mainwindow = ui_mainwindow

        # Crie uma instância da classe ui_analises
        self.ui_analises = Ui_Analises()
        self.ui_analises.setupUi(self)

    def exibir_analises(self):

        # Conecte o clique do botão à função que executa o código desejado
        self.ui_analises.pushButton.clicked.connect(self.analisar_por_data)
        self.ui_analises.pushButton_2.clicked.connect(self.analisar_por_acao)
        self.ui_analises.pushButton_3.clicked.connect(self.analisar_por_periodo_hoje)
        self.ui_analises.pushButton_4.clicked.connect(self.analisar_por_periodo_amanha)
        self.ui_analises.pushButton_5.clicked.connect(self.analisar_por_periodo_essa_semana)
        self.ui_analises.pushButton_6.clicked.connect(self.analisar_por_periodo_pro_semana)
        
        self.show()
    def analisar_por_data(self):
        # Define o dia de hoje"
        hoje = self.ui_analises.dateEdit.date().toString("dd.MM.yyyy")
        tabela = 'tabela_' + hoje

        # Lista para armazenar os resultados de todas as consultas
        all_results = []
        lista_valor_dinamico = []

        self.testagem = Testagem_Yfinance(self.host, self.user, self.password, self.database)
        valor_dinamico = self.testagem.testagem_automatica(hoje)
        lista_valor_dinamico.append(valor_dinamico)

        # -----------------   Atualiza Tela com as informações analisadas ------------- 
            
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT * FROM `{tabela}`")

            # Recupere os resultados
            result = cursor.fetchall()

            # Índice da coluna específica a ser usada para ordenar todas as colunas
            coluna_index_para_ordenacao = 8

            # Classificar os dados com base nos valores da coluna específica
            day_results = sorted(result, key=lambda x: float(x[coluna_index_para_ordenacao]) if x[coluna_index_para_ordenacao] else float('-inf'), reverse=True)

            # Adicione os resultados à lista
            all_results.extend(day_results)

            # Preencha a tabela na janela de "Análises"
            self.ui_analises.tableWidget.setRowCount(len(all_results))
            for row_index, row_data in enumerate(all_results):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui_analises.tableWidget.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")
        finally:
            # Feche a conexão com o banco de dados
            cursor.close()
            db.close()
            print(lista_valor_dinamico)  
           
    def analisar_por_acao(self):
            
            simbolo_da_acao = self.ui_analises.lineEdit.text()
            
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            try:
                # Criar um cursor para executar consultas SQL
                cursor = db.cursor()

                # Consultar as tabelas no banco de dados
                cursor.execute("SHOW TABLES")

                # Obter resultados da consulta
                tabelas = cursor.fetchall()

                # Exibir as tabelas encontradas
                if tabelas:
                    print("Tabelas no banco de dados:")
                    for tabela in tabelas:
                        print(tabela[0])
                else:
                    print("Nenhuma tabela encontrada no banco de dados.")

            finally:
                # Fechar o cursor e a conexão
                cursor.close()
                db.close()

            # -----------------   Pegar dados da API Yfinance -------------
            try: 

                self.testagem = Testagem_Yfinance(self.host, self.user, self.password, self.database)
                
                # Análise de preço da ação encontrada

                valor_da_acao = self.testagem.testagem_preco(simbolo_da_acao)
                print(valor_da_acao)
                
                # Análise frequancia de dividendos da empresa
                
                frequencia_da_acao = self.testagem.testagem_frequencia_de_dividendos(simbolo_da_acao)
                print(frequencia_da_acao)

                # Análise de moeda da ação
                    
                moeda = self.testagem.testagem_moeda_da_acao(simbolo_da_acao)
                print(moeda)
            except:
                # Análise de preço da ação encontrada
                simbolo_da_acao_BRL = simbolo_da_acao + '.SA'

                valor_da_acao = self.testagem.testagem_preco(simbolo_da_acao_BRL)
                print(valor_da_acao)
                
                # Análise frequancia de dividendos da empresa
                
                frequencia_da_acao = self.testagem.testagem_frequencia_de_dividendos(simbolo_da_acao_BRL)
                print(frequencia_da_acao)

                # Análise de moeda da ação
                    
                moeda = self.testagem.testagem_moeda_da_acao(simbolo_da_acao_BRL)
                print(moeda)

    def analisar_por_periodo_hoje(self):
        
        # Verifique se hoje é sábado ou domingo
        data_objeto = datetime.now()
        dia_semana = data_objeto.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo
        # Define o dia de hoje
        data_ex = data_objeto.strftime("%d.%m.%Y")


        tabela = 'tabela_' + data_ex

        if dia_semana == 5 or dia_semana == 6:  # 5 é sábado, 6 é domingo
            # Mostra uma mensagem informando que é fim de semana
            QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
            return
        
        # Método para coletar dados da tabela de dividendos do dia

        self.testagem = Testagem_Yfinance(self.host, self.user, self.password, self.database)
        simbolos_encontrados = self.testagem.testagem_por_data_encontrados(data_ex)
        simbolos_encontrados_com_sa = self.testagem.testagem_por_data_nao_encontrados(data_ex)

        print('Símbolos Encontrados')
        print(simbolos_encontrados)
        print('Símbolos não Encontrados')
        print(simbolos_encontrados_com_sa)


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

        self.atualizacao = Atualizar_Tabelas()

        # Análise de preço da ação encontrada

        print(simbolos_encontrados)

        for simbolo in simbolos_encontrados:

            valor_da_acao = self.testagem.testagem_preco(simbolo)
        # Análise frequancia de dividendos da empresa
            frequencia_da_acao = self.testagem.testagem_frequencia_de_dividendos(simbolo)
            self.atualizacao.atualizar_tabela_dividendos_frequencia(tabela, simbolo, frequencia_da_acao)
        # Análise de moeda da ação
            moeda = self.testagem.testagem_moeda_da_acao(simbolo)
            self.atualizacao.atualizar_tabela_dividendos_moeda(tabela, simbolo, moeda)
        # Análise Relação Dividendo por Valor da Ação
            relacao = self.testagem.extrair_relacao_dividendo_valor_da_acao(tabela, simbolo, valor_da_acao)
            self.atualizacao.atualizar_tabela_dividendos_relacao(tabela, simbolo, relacao)

        # -----------------   Pegar linha a linha de acordo com a lista de não encontrados -------------

        # Análise de preço da ação encontrada
            
        print(simbolos_encontrados_com_sa)

        for simbolo in simbolos_encontrados_com_sa:
            try:

                valor_da_acao = self.testagem.testagem_preco(simbolo + '.SA')
                print(valor_da_acao)
            # Análise frequancia de dividendos da empresa
                frequencia_da_acao_de_não_encontradas = self.testagem.testagem_frequencia_de_dividendos(simbolo + '.SA')
                print(frequencia_da_acao_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_frequencia(tabela, simbolo, frequencia_da_acao_de_não_encontradas)
            # Análise de moeda da ação
                moeda_de_não_encontradas = self.testagem.testagem_moeda_da_acao(simbolo + '.SA')
                print(moeda_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_moeda(tabela, simbolo, moeda_de_não_encontradas)
            # Análise Relação Dividendo por Valor da Ação
                relacao_de_não_encontradas = self.testagem.extrair_relacao_dividendo_valor_da_acao(tabela, simbolo, valor_da_acao)
                print('A relação do valor da ação pelo dividendo é: ', relacao_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_relacao(tabela, simbolo, relacao_de_não_encontradas)
            except:
                continue
        
        # -----------------   Atualiza Tela com as informações analisadas -------------   
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT * FROM `{tabela}`")

            # Recupere os resultados
            result = cursor.fetchall()

            # Preencha a tabela na janela de "Análises"
            self.ui_analises.tableWidget_2.setRowCount(len(result))
            for row_index, row_data in enumerate(result):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui_analises.tableWidget_2.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()

    def analisar_por_periodo_amanha(self):
        # Verifique se hoje é sábado ou domingo
        data_objeto = datetime.now()
        dia_amanha = data_objeto + timedelta(days=1)
        
        dia_semana = data_objeto.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo
        # Define o dia de hoje
        data_ex = data_objeto.strftime("%d.%m.%Y")


        tabela = 'tabela_' + data_ex

        if dia_semana == 4 or dia_semana == 5:  # 4 é sexta, 5 é sábado
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
        
        # Método para coletar dados da tabela de dividendos do dia

        self.testagem = Testagem_Yfinance(self.host, self.user, self.password, self.database)
        simbolos_encontrados = self.testagem.testagem_por_data_encontrados(data_ex)
        simbolos_encontrados_com_sa = self.testagem.testagem_por_data_nao_encontrados(data_ex)

        print('Símbolos Encontrados')
        print(simbolos_encontrados)
        print('Símbolos não Encontrados')
        print(simbolos_encontrados_com_sa)


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

        self.atualizacao = Atualizar_Tabelas()

        # Análise de preço da ação encontrada

        print(simbolos_encontrados)

        for simbolo in simbolos_encontrados:

            valor_da_acao = self.testagem.testagem_preco(simbolo)
        # Análise frequancia de dividendos da empresa
            frequencia_da_acao = self.testagem.testagem_frequencia_de_dividendos(simbolo)
            self.atualizacao.atualizar_tabela_dividendos_frequencia(tabela, simbolo, frequencia_da_acao)
        # Análise de moeda da ação
            moeda = self.testagem.testagem_moeda_da_acao(simbolo)
            self.atualizacao.atualizar_tabela_dividendos_moeda(tabela, simbolo, moeda)
        # Análise Relação Dividendo por Valor da Ação
            relacao = self.testagem.extrair_relacao_dividendo_valor_da_acao(tabela, simbolo, valor_da_acao)
            self.atualizacao.atualizar_tabela_dividendos_relacao(tabela, simbolo, relacao)

        # -----------------   Pegar linha a linha de acordo com a lista de não encontrados -------------

        # Análise de preço da ação encontrada
            
        print(simbolos_encontrados_com_sa)

        for simbolo in simbolos_encontrados_com_sa:
            try:

                valor_da_acao = self.testagem.testagem_preco(simbolo + '.SA')
                print(valor_da_acao)
            # Análise frequancia de dividendos da empresa
                frequencia_da_acao_de_não_encontradas = self.testagem.testagem_frequencia_de_dividendos(simbolo + '.SA')
                print(frequencia_da_acao_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_frequencia(tabela, simbolo, frequencia_da_acao_de_não_encontradas)
            # Análise de moeda da ação
                moeda_de_não_encontradas = self.testagem.testagem_moeda_da_acao(simbolo + '.SA')
                print(moeda_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_moeda(tabela, simbolo, moeda_de_não_encontradas)
            # Análise Relação Dividendo por Valor da Ação
                relacao_de_não_encontradas = self.testagem.extrair_relacao_dividendo_valor_da_acao(tabela, simbolo, valor_da_acao)
                print('A relação do valor da ação pelo dividendo é: ', relacao_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_relacao(tabela, simbolo, relacao_de_não_encontradas)
            except:
                continue
        
        # -----------------   Atualiza Tela com as informações analisadas -------------   
        try:
           # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT * FROM `{tabela}`")

            # Recupere os resultados
            result = cursor.fetchall()

            # Preencha a tabela na janela de "Análises"
            self.ui_analises.tableWidget_2.setRowCount(len(result))
            for row_index, row_data in enumerate(result):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.ui_analises.tableWidget_2.setItem(row_index, col_index, item)

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()
    
    def analisar_por_periodo_essa_semana(self):
        # Define o dia de hoje
        data_objeto = datetime.now()

        # Lista para armazenar os resultados de todas as consultas
        all_results = []

        for i in range(7):  # Loop pelos dias da semana (0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo)
            # Pula os sábados (5) e domingos (6)
            print(i)
            if i == 5 or i == 6:
                continue
            
            # Atribui o dia da semana para efetuar deslocamento
            dia_da_semana = data_objeto.weekday()
            # Busca dia para efetuar o deslocamento
            desloc = self.switch_case_numero_dia_da_semana2(dia_da_semana)
            # Efetua o deslocamento da data
            dia_semana_atual = data_objeto + timedelta(days= i - desloc)
            # Define o dia para o loop
            data_ex = dia_semana_atual.strftime("%d.%m.%Y")


            tabela = 'tabela_' + data_ex
        
            # Método para coletar dados da tabela de dividendos do dia

            self.testagem = Testagem_Yfinance(self.host, self.user, self.password, self.database)
            self.testagem.testagem_automatica(data_ex)

            # -----------------   Atualiza Tela com as informações analisadas -------------   
            try:
                # Conecte ao banco de dados MySQL
                db = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                
                cursor = db.cursor()

                # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                cursor.execute(f"SELECT * FROM `{tabela}`")

                # Recupere os resultados
                result = cursor.fetchall()

                # Adicione os resultados à lista
                all_results.extend(result)

                # Preencha a tabela na janela de "Análises"
                self.ui_analises.tableWidget_2.setRowCount(len(all_results))
                for row_index, row_data in enumerate(result):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.ui_analises.tableWidget_2.setItem(row_index, col_index, item)
            except mysql.connector.Error as err:
                # Handle the error (e.g., table not found)
                print(f"Error: {err}")
            finally:
                # Feche a conexão com o banco de dados
                cursor.close()
                db.close()

    def analisar_por_periodo_pro_semana(self):
        # Define o dia de hoje
        data_objeto = datetime.now()
        days_number = data_objeto.weekday()
        end_day = self.switch_case_numero_dia_da_semana1(days_number)
        start_day = self.switch_case_numero_dia_da_semana0(days_number)
        print(start_day, end_day)

        # Lista para armazenar os resultados de todas as consultas
        all_results = []
        lista_valor_dinamico = []

        for i in range(start_day, end_day):  # Loop pelos dias da próxima semana

            # Atribui o dia da semana para efetuar deslocamento
            dia_semana_proxima = data_objeto + timedelta(days=i)
            # Define o dia para o loop
            data_dia_semana_proxima = dia_semana_proxima.strftime("%d.%m.%Y")

            # Pula os sábados (5) e domingos (6)
            conf_data = dia_semana_proxima.weekday()
            if conf_data == 5 or conf_data == 6:
                continue



            tabela = 'tabela_' + data_dia_semana_proxima
        
            # Método para coletar dados da tabela de dividendos do dia

            self.testagem = Testagem_Yfinance(self.host, self.user, self.password, self.database)
            valor_dinamico = self.testagem.testagem_automatica(data_dia_semana_proxima)
            lista_valor_dinamico.append(valor_dinamico)

            # -----------------   Atualiza Tela com as informações analisadas ------------- 
              
            try:
                # Conecte ao banco de dados MySQL
                db = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                
                cursor = db.cursor()

                # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                cursor.execute(f"SELECT * FROM `{tabela}`")

                # Recupere os resultados
                result = cursor.fetchall()

                # Índice da coluna específica a ser usada para ordenar todas as colunas
                coluna_index_para_ordenacao = 8

                # Classificar os dados com base nos valores da coluna específica
                day_results = sorted(result, key=lambda x: float(x[coluna_index_para_ordenacao]) if x[coluna_index_para_ordenacao] else float('-inf'), reverse=True)

                # Adicione os resultados à lista
                all_results.extend(day_results)

                # Preencha a tabela na janela de "Análises"
                self.ui_analises.tableWidget_2.setRowCount(len(all_results))
                for row_index, row_data in enumerate(all_results):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.ui_analises.tableWidget_2.setItem(row_index, col_index, item)

            except mysql.connector.Error as err:
                # Handle the error (e.g., table not found)
                print(f"Error: {err}")
            finally:
                # Feche a conexão com o banco de dados
                cursor.close()
                db.close()
                print(lista_valor_dinamico)
  
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
