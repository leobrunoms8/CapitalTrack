import yfinance as yf

class Analise_De_Simbolos:
    def __init__(self, lista_simbolos):
        self.lista_simbolos = lista_simbolos
        self.simbolos_encontrados = []
        self.simbolos_nao_encontrados = []

    def verificar_simbolos(self):
        for linha in self.lista_simbolos:
            try:
                # Imprime qual Siímbolo está sendo Analisado no momento

                print("Analisando: '",linha,"'")

                # Tenta criar um objeto Ticker para o símbolo
                acao = yf.Ticker(linha)

                # Obtém os dados históricos mais recentes (último dia)
                dados_historicos = acao.history(period='1d')

                # Obtém o preço de fechamento mais recente
                ultimo_preco_fechamento = dados_historicos['Close'].iloc[-1]
                print(ultimo_preco_fechamento)

                # Adiciona o símbolo aos símbolos encontrados
                self.simbolos_encontrados.append(linha)

            except Exception as e:
                     # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                    self.simbolos_nao_encontrados.append(linha)
                    print(f"Erro ao obter o nome da empresa para o símbolo {linha}: {e}")
               
    def obter_resultados(self):
        return {
            'simbolos_encontrados': self.simbolos_encontrados,
            'simbolos_nao_encontrados': self.simbolos_nao_encontrados
        }

