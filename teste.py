import yfinance as yf
import mplfinance as mpf

# Função para plotar candlesticks com base em datas específicas
def plot_candlesticks(symbol, start_date, end_date):
    # Obter dados históricos do Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Plotar candlesticks usando mplfinance
    mpf.plot(data, type='candle', style='charles', volume=True)

# Data ex da ação e data ex antecessora
data_ex = '2023-01-01'
data_ex_antecessora = '2022-01-01'

# Símbolo da ação
symbol = 'AAPL'  # Altere para o símbolo da ação desejada

# Chamar a função para plotar candlesticks
plot_candlesticks(symbol, data_ex_antecessora, data_ex)
