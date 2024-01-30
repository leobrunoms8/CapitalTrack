from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from datetime import datetime
import mysql.connector

from .FrontEnd.Interface.Window_Analises import Ui_Analises
from .Metodos.Testagem_Yfinance_por_data import Testagem_Yfinance
from .Metodos.Apagar_Tabela_Generico import ApagarTabelaGenerico
from .Metodos.Criar_Tabela_Generico import CriarTabelaGenerico
from .Metodos.Atualizar_Tabelas import Atualizar_Tabelas

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
        self.ui_analises.pushButton_3.clicked.connect(self.analisar_por_periodo_hoje)
        self.ui_analises.pushButton_4.clicked.connect(self.analisar_por_periodo_amanha)
        self.ui_analises.pushButton_5.clicked.connect(self.analisar_por_periodo_essa_semana)
        self.ui_analises.pushButton_6.clicked.connect(self.analisar_por_periodo_pro_semana)
        
        self.show()
    def analisar_por_data(self):
            # Verifique se hoje é sábado ou domingo
            data_ex = self.ui_analises.dateEdit.date().toString("dd.MM.yyyy")
            data_formato = "%d.%m.%Y"
            data_objeto = datetime.strptime(data_ex, data_formato)
            dia_semana = data_objeto.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo
            # Define o dia de hoje
            tabela = 'tabela_' + data_ex

            if dia_semana == 5 or dia_semana == 6:  # 5 é sábado, 6 é domingo
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
            
            # Método para coletar dados da tabela de dividendos do dia

            self.testagem = Testagem_Yfinance()
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

            for simbolo in simbolos_encontrados_com_sa:

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
                print('Arelação do valor da ação pelo dividendo é: ', relacao_de_não_encontradas)
                self.atualizacao.atualizar_tabela_dividendos_relacao(tabela, simbolo, relacao_de_não_encontradas)
            
            # -----------------   Atualizar banco de dados com as informações analisadas -------------   
           
    def analisar_por_acao(self):
            
            simbolo_da_acao = self.ui_analises.lineEdit.text()
            
             # Estabelecer conexão com o banco de dados
            conexao = mysql.connector.connect(
                    host="localhost",
                    user="developer",
                    password="Leo140707",
                    database="RaspagemPuraDeDados"
                )
            
            try:
                # Criar um cursor para executar consultas SQL
                cursor = conexao.cursor()

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
                conexao.close()


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

            # -----------------   Pegar dados da API Yfinance -------------

            self.testagem = Testagem_Yfinance()
            
            # Análise de preço da ação encontrada

            valor_da_acao = self.testagem.testagem_preco(simbolo_da_acao)
            print(valor_da_acao)
            
            # Análise frequancia de dividendos da empresa
            
            frequencia_da_acao = self.testagem.testagem_frequencia_de_dividendos(simbolo_da_acao)
            print(frequencia_da_acao)

            # Análise de moeda da ação
                
            moeda = self.testagem.testagem_moeda_da_acao(simbolo_da_acao)
            print(moeda)

    def analisar_por_periodo_hoje(self):
        
        # Verifique se hoje é sábado ou domingo
        data_ex = datetime.now()
        data_formato = "%d.%m.%Y"
        data_objeto = datetime.strptime(data_ex, data_formato)
        dia_semana = data_objeto.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo
        # Define o dia de hoje
        tabela = 'tabela_' + data_ex

        if dia_semana == 5 or dia_semana == 6:  # 5 é sábado, 6 é domingo
            # Mostra uma mensagem informando que é fim de semana
            QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
            return
        
        # Método para coletar dados da tabela de dividendos do dia

        self.testagem = Testagem_Yfinance()
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

        for simbolo in simbolos_encontrados_com_sa:

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
            print('Arelação do valor da ação pelo dividendo é: ', relacao_de_não_encontradas)
            self.atualizacao.atualizar_tabela_dividendos_relacao(tabela, simbolo, relacao_de_não_encontradas)
        
        # -----------------   Atualiza Tela com as informações analisadas -------------   
        try:
            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Execute uma consulta para obter dados da tabela correspondente à data escolhida
            cursor.execute(f"SELECT * FROM {tabela}")

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
            hoje = datetime.now()
            dia_semana = hoje.weekday()  # 0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo

            if dia_semana == 4 or dia_semana == 5:  # 4 é sexta, 5 é sábado
                # Mostra uma mensagem informando que é fim de semana
                QMessageBox.warning(self, "Aviso", "Hoje é fim de semana. Não há consulta de dividendos disponível.")
                return
        
            try:
                # Define o dia de amanhã
                hoje = datetime.now()
                dia_amanha = hoje + timedelta(days=1)
                data_amanha = dia_amanha.strftime("%d.%m.%Y")
                tabela_nome = f"`tabela_{data_amanha}`"

                # Conecte ao banco de dados MySQL
                db = mysql.connector.connect(
                    host="localhost",
                    user="developer",
                    password="Leo140707",
                    database="RaspagemPuraDeDados"
                )

                cursor = db.cursor()

                # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                cursor.execute(f"SELECT * FROM {tabela_nome}")

                # Recupere os resultados
                result = cursor.fetchall()

                # Preencha a tabela na janela de "Dividendos"
                self.ui_dividendos.tableWidget_3.setRowCount(len(result))
                for row_index, row_data in enumerate(result):
                    for col_index, col_data in enumerate(row_data):
                        item = QTableWidgetItem(str(col_data))
                        self.ui_dividendos.tableWidget_3.setItem(row_index, col_index, item)

            except mysql.connector.Error as err:
                # Handle the error (e.g., table not found)
                print(f"Error: {err}")

            finally:
                # Feche a conexão com o banco de dados
                db.close()
    
    def analisar_por_periodo_essa_semana(self):
        try:
            # Define o dia de hoje
            hoje = datetime.now()

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Lista para armazenar os resultados de todas as consultas
            all_results = []

            for i in range(7):  # Loop pelos dias da semana (0 é segunda-feira, 1 é terça-feira, ..., 6 é domingo)
                # Pula os sábados (5) e domingos (6)
                print(i)
                if i == 5 or i == 6:
                    continue

                # Calcula a data para o dia da semana atual
                dia_p_desloc = hoje.weekday()
                desloc = self.switch_case_numero_dia_da_semana2(dia_p_desloc)
                dia_semana_atual = hoje + timedelta(days= i - desloc)
                data_dia_semana_atual = dia_semana_atual.strftime("%d.%m.%Y")
                tabela_nome = f"`tabela_{data_dia_semana_atual}`"

                try:
                    # Execute a consulta para obter dados da tabela correspondente à data escolhida
                    cursor.execute(f"SELECT * FROM {tabela_nome}")

                    # Recupere os resultados
                    result = cursor.fetchall()

                    # Adicione os resultados à lista
                    all_results.extend(result)

                    # Preencha a tabela na janela de "Dividendos"
                    self.ui_dividendos.tableWidget_4.setRowCount(len(all_results))
                    for row_index, row_data in enumerate(all_results):
                        for col_index, col_data in enumerate(row_data):
                            item = QTableWidgetItem(str(col_data))
                            self.ui_dividendos.tableWidget_4.setItem(row_index, col_index, item)
                except mysql.connector.Error as err:
                    # Handle the error (e.g., table not found)
                    print(f"Error: {err}")
                    continue

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")


        finally:
            # Feche a conexão com o banco de dados
            db.close()

    def analisar_por_periodo_pro_semana(self):
        try:
            # Define o dia de hoje
            hoje = datetime.now()

            # Exemplo de uso
            days_number = hoje.weekday()
            end_day = self.switch_case_numero_dia_da_semana1(days_number)
            start_day = self.switch_case_numero_dia_da_semana0(days_number)
            print(start_day, end_day)

            # Conecte ao banco de dados MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="developer",
                password="Leo140707",
                database="RaspagemPuraDeDados"
            )

            cursor = db.cursor()

            # Lista para armazenar os resultados de todas as consultas
            all_results = []

            for i in range(start_day, end_day):  # Loop pelos dias da próxima semana
                
                # Calcula a data para o dia da semana próxima semana
                dia_semana_proxima = hoje + timedelta(days=i)
                data_dia_semana_proxima = dia_semana_proxima.strftime("%d.%m.%Y")
                print(data_dia_semana_proxima)
                tabela_nome = f"`tabela_{data_dia_semana_proxima}`"

                # Pula os sábados (5) e domingos (6)
                conf_data = dia_semana_proxima.weekday()
                if conf_data == 5 or conf_data == 6:
                    continue
                
                try:
                    # Execute a consulta para obter dados da tabela correspondente à data escolhida
                    cursor.execute(f"SELECT * FROM {tabela_nome}")

                    # Recupere os resultados
                    result = cursor.fetchall()

                    # Adicione os resultados à lista
                    all_results.extend(result)

                    # Preencha a tabela na janela de "Dividendos"
                    self.ui_dividendos.tableWidget_5.setRowCount(len(all_results))
                    for row_index, row_data in enumerate(all_results):
                        for col_index, col_data in enumerate(row_data):
                            item = QTableWidgetItem(str(col_data))
                            self.ui_dividendos.tableWidget_5.setItem(row_index, col_index, item)
                except mysql.connector.Error as err:
                    # Handle the error (e.g., table not found)
                    print(f"Error: {err}")
                    continue                

        except mysql.connector.Error as err:
            # Handle the error (e.g., table not found)
            print(f"Error: {err}")

        finally:
            # Feche a conexão com o banco de dados
            db.close()
    
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
