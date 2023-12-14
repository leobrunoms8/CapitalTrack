from datetime import datetime, timedelta

class CalculadoraDatas:
    def __init__(self):
        self.hoje = datetime.now()

    def obter_hoje(self):
        return self.hoje.strftime("%Y.%m.%d")

    def obter_amanha(self):
        amanha = self.hoje + timedelta(days=1)
        return amanha.strftime("%Y.%m.%d")

    def obter_dias_da_semana_atual(self):
        dias_da_semana = []
        for i in range(7 - self.hoje.weekday()):
            dia = self.hoje + timedelta(days=i)
            dias_da_semana.append(dia.strftime("%Y.%m.%d"))
        return dias_da_semana

    def obter_dias_da_proxima_semana(self):
        dias_da_semana = []
        proxima_semana = self.hoje + timedelta(days=(7 - self.hoje.weekday()) + 7)
        for i in range(5):  # 5 dias de segunda a sexta
            dia = proxima_semana + timedelta(days=i)
            dias_da_semana.append(dia.strftime("%Y.%m.%d"))
        return dias_da_semana

