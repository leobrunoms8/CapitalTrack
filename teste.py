import yfinance as yf

# Símbolo da ação da Vale
simbolo = "VALE3.SA"

# Criar um objeto Ticker para a ação da Vale
acao_vale = yf.Ticker(simbolo)

# Obter os dados históricos mais recentes (último dia)
dados_historicos = acao_vale.history(period='1d')

# Obter o preço de fechamento mais recente
ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]

print(f"O preço atual da ação VALE3 é: R$ {ultimo_preco_fechamento:.2f}")
