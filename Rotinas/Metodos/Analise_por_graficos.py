import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


from datetime import datetime

# Função para obter dados históricos de uma ação
def obter_dados_acao(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def obter_periodo_entre_datas_ex(symbol):
    # Obtendo os dividendos da ação
    acao = yf.Ticker(symbol)
    dividendos_acao = acao.dividends

    # Remover informações de fuso horário do índice
    dividendos_acao.index = dividendos_acao.index.tz_localize(None)

    # Lista de períodos
    periodos = []
    for i in range(len(dividendos_acao) - 1):
        periodo_atual = [dividendos_acao.index[i + 1], dividendos_acao.index[i]]
        periodos.append(periodo_atual)

    # Lista de períodos
    periodos_formatados = []
    for periodo in periodos:
        periodo_formatado = [datetime.strftime(data, "%Y-%m-%d") for data in periodo]
        periodos_formatados.append(periodo_formatado)

    return periodos_formatados

def calcular_quantidade_dias(dados, data_final):
    # Calcula a quantidade de dias entre a data de início e a data final
    quantidade_dias_total = (data_final - dados.index[0]).days
    return quantidade_dias_total

def encontrar_menor_valor(dados):
    # Encontra o menor valor na série temporal de preços
    menor_valor = dados['Close'].min()
    dia_menor_valor = dados[dados['Close'] == menor_valor].index[0]
    return menor_valor, dia_menor_valor

def calcular_quantidade_dias_menor_valor(data1, data2):
    # Convertendo as strings em objetos datetime
    data1_obj = datetime.strptime(data1, '%Y-%m-%d')
    data2_obj = datetime.strptime(data2, '%Y-%m-%d')
    
    # Calculando a diferença em dias
    diferenca = abs((data2_obj - data1_obj).days)
    
    return diferenca

def plotar_curvas_e_fechamento_linha(data):
    # Criando o gráfico
    plt.figure(figsize=(10, 6))

    # Plotando as curvas anteriores (se estiverem presentes)
    plt.plot(data.index, data['macd'], label='MACD')

    # Plotando os valores de fechamento da ação
    plt.plot(data.index, data['Close'], label='Fechamento', color='black')

    # Adicionando legendas, título e rótulos dos eixos
    plt.legend()
    plt.title('Análise Técnica e Fechamento da Ação')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    
    # Exibindo o gráfico
    plt.grid(True)
    plt.show()

def plotar_curvas_e_fechamento_candles(data):
    # Criando o gráfico
    mpf.plot(data, type='candle', style='charles', volume=True, ylabel='Preço', ylabel_lower='Volume')



# Símbolo da ação e intervalo de datas
symbol = 'HRZN'

# Obtenção de períodos para analise
periodos_formatado_para_analise = obter_periodo_entre_datas_ex(symbol)
print(periodos_formatado_para_analise)

for periodo in periodos_formatado_para_analise:

    try: 
        start_date = periodo[1]
        end_date = periodo[0]

        date_timestamp = pd.to_datetime(end_date)  # Convertendo a string para Timestamp
        # Subtrai um dia do Timestamp
        timestamp_subtracao = date_timestamp - pd.Timedelta(days=1)

        # Converte o Timestamp de volta para uma string
        new_end_date = timestamp_subtracao.strftime('%Y-%m-%d')

        # Obtendo dados históricos
        data = obter_dados_acao(symbol, start_date, new_end_date)
        quantidade_de_dias_por_periodo = calcular_quantidade_dias(data, timestamp_subtracao)
        menor_valor_por_periodo, data_menor_valor = encontrar_menor_valor(data)
        dias_menor_valor_p_data_ex = calcular_quantidade_dias_menor_valor((data_menor_valor.strftime('%Y-%m-%d')), (date_timestamp.strftime('%Y-%m-%d')))
        
        # Calculando algumas métricas de análise técnica
        data['sma_50'] = ta.trend.sma_indicator(data['Close'], window=50)
        data['sma_200'] = ta.trend.sma_indicator(data['Close'], window=200)
        data['rsi'] = ta.momentum.rsi(data['Close'], window=14)
        data['macd'] = ta.trend.macd_diff(data['Close'])

        print(data.tail())
        print('Quandidade de dias por período é: ', quantidade_de_dias_por_periodo)
        print('O menor valor no período é: ', menor_valor_por_periodo)
        print('O menor valor ocorreu no dia: ', data_menor_valor)
        print('O menor valor acontece a: ', dias_menor_valor_p_data_ex)
        
        # Plotar Graficos dos períodos entre Datas Ex
        plotar_curvas_e_fechamento_linha(data)
        plotar_curvas_e_fechamento_candles(data)
    except:
        continue