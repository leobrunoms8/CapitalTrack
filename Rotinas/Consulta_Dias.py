from Calculos.Dia_Hoje_Amanha_ProximaSemana import CalculadoraDatas

# Classe que executa o método
class ExecutarCalculadora:
    def __init__(self, calculadora):
        self.calculadora = calculadora

    def executar(self):
        print("Hoje é:", self.calculadora.obter_hoje())
        print("Amanhã é:", self.calculadora.obter_amanha())

        dias_da_semana_atual = self.calculadora.obter_dias_da_semana_atual()
        print("Dias da semana atual:")
        for dia in dias_da_semana_atual:
            print(dia)

        dias_da_proxima_semana = self.calculadora.obter_dias_da_proxima_semana()
        print("Dias da próxima semana:")
        for dia in dias_da_proxima_semana:
            print(dia)

# Criar instância da calculadora
calculadora = CalculadoraDatas()

# Criar instância da classe executadora e executar
executador = ExecutarCalculadora(calculadora)
executador.executar()


