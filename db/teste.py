import yfinance as yf

def obter_preco_acao(ticker):
    # Cria um objeto Ticker para a ação desejada
    acao = yf.Ticker(ticker)

    # Obtém os dados históricos mais recentes (último dia)
    dados_historicos = acao.history(period='1d')

    # Obtém o preço de fechamento mais recente
    ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]

    return ultimo_preco_fechamento

# Substitua 'AAPL' pelo símbolo da ação desejada
ticker_acao = 'BGH'

# Obtém e imprime o preço da ação
preco_acao = obter_preco_acao(ticker_acao)
print(f"O preço atual da ação {ticker_acao} é: {preco_acao}")
