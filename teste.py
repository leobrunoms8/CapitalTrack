 # Executar ao clicar no pushButton_2
        url = "https://br.investing.com/dividends-calendar/"
        raspagem = RaspagemInvesting(url)
        raspagem.realizar_raspagem()

# Codigo da classe main



            
            for simbolo in simbolos_encontrados:
                try:
                    print(simbolo)
                    # Conecte ao banco de dados MySQL
                    db = mysql.connector.connect(
                        host="localhost",
                        user="developer",
                        password="Leo140707",
                        database="RaspagemPuraDeDados"
                    )

                    cursor = db.cursor()

                    # Execute uma consulta para obter dados da tabela correspondente à data escolhida
                    cursor.execute(f"SELECT valor_dividendo FROM {tabela_nome} WHERE simbolo = '{simbolo}'")

                    # Recupere os resultados
                    resultados_dos_valores = cursor.fetchall()
                    print(resultados_dos_valores)

                    # Encontrar a posição da primeira vírgula
                    primeira_virgula = str(resultados_dos_valores).find(',')
                    
                    # Encontrar a posição da segunda vírgula a partir da posição da primeira vírgula
                    segunda_virgula = str(resultados_dos_valores).find(',', primeira_virgula + 1)

                    # Criar uma nova string excluindo-a
                    nova_string = str(resultados_dos_valores)[:segunda_virgula] + str(resultados_dos_valores)[segunda_virgula+1:]

                    # Remova caracteres desnecessários
                    string_limpa = nova_string.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "")

                    # Substitua a vírgula pelo ponto como separador decimal
                    string_numerica = string_limpa.replace(',', '.')

                    # Converta a string numérica para float
                    try:
                        numero_float = float(string_numerica)
                    except ValueError as erro:
                        print(string_numerica)
                        continue


                    print(numero_float)

                    # Consulta a moeda do dividendo
                    # Tenta criar um objeto Ticker para o símbolo
                    acao = yf.Ticker(simbolo)

                    # Tenta obter as informações importantes da ação
                    # Moeda da ação

                    fast_info = acao.get_fast_info()
                    moeda = fast_info['currency']
                    print(moeda)
                    if moeda == 'USD':
                        # Multiplicar pela cotação atual
                        # Criar um objeto CurrencyRates
                        c = CurrencyRates()

                        # Obter a taxa de câmbio USD para BRL
                        taxa_usd_brl = c.get_rate('USD', 'BRL')

                        # Imprimir a taxa de câmbio
                        print(f"A taxa de câmbio USD/BRL é: {taxa_usd_brl}")

                        dividendo_em_BRL = taxa_usd_brl * numero_float
                        print(f'O valor do dividendo em reais é: {dividendo_em_BRL}')

                        
                    elif moeda == 'BRL':
                        # Apenas imprimir na tela
                        print(numero_float)
                    
                    # Relação Dividendo/Ação
                    # Obtém os dados históricos mais recentes (último dia)
                    dados_historicos = acao.history(period='1d')

                    # Obtém o preço de fechamento mais recente
                    preco_acao = dados_historicos['Close'].iloc[-1]

                    relacao_div_acao = numero_float / preco_acao

                    print(relacao_div_acao)
                        
                except mysql.connector.Error as erro:
                    print(f"Erro ao consultar a tabela: {erro}")
            # Anexar as novas informações a tabela rascunho
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
                    cursor.execute(f"SELECT id, nome_empresa, data_ex, data_pagamento FROM {tabela_nome} WHERE simbolo = '{simbolo}'")

                    # Recupere os resultados
                    resultados_dos_valores = cursor.fetchall()
                    print(resultados_dos_valores)

                except mysql.connector.Error as erro:
                    print(f"Erro ao consultar a tabela: {erro}")

                for simbolo in simbolos_encontrados:
                    try:
                        print("Analisando: '",simbolo,"'")

                        # Tenta criar um objeto Ticker para o símbolo
                        acao = yf.Ticker(simbolo)

                        # Tenta obter as informações importantes da ação
                        # Moeda da ação

                        fast_info = acao.get_fast_info()
                        moeda = fast_info['currency']
                        print(moeda)

                        # Dividendos

                        dividendos_acao = acao.get_dividends()
                        print(dividendos_acao)

                    except Exception as e:
                        # Se ocorrer um erro, exibe o erro e continua
                        print(f"Erro ao consultar simbolo {simbolo}: {e}")
                        continue

                    # Preencha a tabela na janela de "Dividendos"
                    self.ui_analises.tableWidget.setRowCount(len(resultados))
                    for row_index, row_data in enumerate(resultados):
                        for col_index, col_data in enumerate(row_data):
                            item = QTableWidgetItem(str(col_data))
                            self.ui_analises.tableWidget.setItem(row_index, col_index, item)