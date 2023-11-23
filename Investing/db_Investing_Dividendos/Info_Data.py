class InfoList:
    def __init__(self, data):
        self.data = data

    def print_info(self):
        total_linhas = len(self.data)
        total_colunas = len(self.data[0]) if self.data else 0

        print(f"Quantidade de Linhas: {total_linhas}")
        print(f"Quantidade de Colunas: {total_colunas}")

