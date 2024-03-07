
from .Raspagem_e_Separacao import Raspagem_e_Separacao_Investing
from .Atualizar_Tabelas import Atualizar_Tabelas

class Gerenciador_Modo_Automatico:
    def __init__(self, host, user, password, database):
        self
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        # Horários para execução dos métodos
        self.horarios_execucao = [
            "09:00:00",  # Método 1
            "12:30:00",  # Método 2
            "22:52:00"   # Método 3
        ]

    def atualizar_data_hora(self, hora_atual, data_hora_log):
        
        if hora_atual in self.horarios_execucao:
            # Chama o método correspondente ao horário atual
            indice = self.horarios_execucao.index(hora_atual) + 1
            metodo = getattr(self, f"metodo_{indice}", None)
            if metodo:
                texto = metodo(data_hora_log)
                return texto
        else:
            return "Aguandando Proximo Método"

    # Métodos fictícios a serem executados em horários específicos
    def metodo_1(self, data_hora):
        print("Método 1 foi acionado às 09:00:00")

    def metodo_2(self, data_hora):
        print("Método 2 foi acionado às 12:30:00")

    def metodo_3(self, data_hora):
        print("Método 3 foi acionado às 22:32:00")
        raspagem = Raspagem_e_Separacao_Investing("timeFrame_nextWeek", self.host, self.user, self.password, self.database)
        raspagem.realizar_raspagem()
        atualizador = Atualizar_Tabelas()
        atualizador.atualizar_log_em_tabela('Raspagem de dividendos da próxima semana do site Investing.com', data_hora)

        return "Método 3 foi acionado às 22:32:00"
