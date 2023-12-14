import yfinance as yf

class Analise_De_Simbolos:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.ultimo_preco_fechamento

    def verificar_ultimo_preco_fechamento(self):
        try:
            # Imprime qual Siímbolo está sendo Analisado no momento

            print("Analisando: '",self.simbolo,"'")

            # Tenta criar um objeto Ticker para o símbolo
            acao = yf.Ticker(self.simbolo)

            # Obtém os dados históricos mais recentes (último dia)
            dados_historicos = acao.history(period='1d')

            # Obtém o preço de fechamento mais recente
            self.ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
            print(self.ultimo_preco_fechamento)

        except Exception as e:
                    # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                print(f"Erro ao consultar simbolo {self.simbolo}: {e}")

        # Retorna o ultimo preço de fechamento solicitado        
        return self.ultimo_preco_fechamento
        
