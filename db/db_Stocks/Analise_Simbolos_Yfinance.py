import yfinance as yf

class Analise_De_Simbolos:
    def __init__(self, lista_simbolos):
        self.lista_simbolos = lista_simbolos
        self.simbolos_encontrados = []
        self.simbolos_nao_encontrados = []

    def verificar_simbolos(self):
        for simbolo in self.lista_simbolos:
            try:
                # Tenta criar um objeto Ticker para o símbolo
                acao = yf.Ticker(simbolo)

                # Tenta obter o nome da empresa associada ao símbolo
                nome_empresa = acao.info['longName']

                # Adiciona o símbolo aos símbolos encontrados
                self.simbolos_encontrados.append({'simbolo': simbolo, 'empresa': nome_empresa})

            except yf.TickerError:
                # Se ocorrer um erro, adiciona o símbolo aos símbolos não encontrados
                self.simbolos_nao_encontrados.append(simbolo)

    def obter_resultados(self):
        return {
            'simbolos_encontrados': self.simbolos_encontrados,
            'simbolos_nao_encontrados': self.simbolos_nao_encontrados
        }

