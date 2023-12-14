class CalculadoraDividendos:
    def __init__(self, preco_acao=None, valor_dividendo=None):
        self.preco_acao = preco_acao
        self.valor_dividendo = valor_dividendo

    def configurar_valores(self, preco_acao, valor_dividendo):
        """
        Configura os valores da ação e do dividendo.

        Parâmetros:
        - preco_acao (float): O preço da ação.
        - valor_dividendo (float): O valor do dividendo.
        """
        self.preco_acao = preco_acao
        self.valor_dividendo = valor_dividendo

    def calcular_relacao_dividendo(self):
        """
        Função para calcular a relação entre o valor da ação e o dividendo.

        Retorna:
        - float: A relação entre o valor do dividendo e o preço da ação, ou None se os valores não estiverem configurados corretamente.
        """
        if self.preco_acao is not None and self.valor_dividendo is not None and self.valor_dividendo != 0:
            relacao = self.valor_dividendo / self.preco_acao
            return relacao
        else:
            return None

