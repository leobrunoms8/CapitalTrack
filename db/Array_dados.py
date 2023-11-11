import re

class DadosParser:
    def __init__(self, dados):
        self.dados = dados
        self.resultados = []

    def processar_dados(self):
        # Padrão para dividir a informação
        padrao = re.compile(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')

        for linha_dados in self.dados:
            # Converter a linha para uma string (caso seja uma lista)
            informacao = ' '.join(map(str, linha_dados))

            # Aplicar o padrão à string
            correspondencia = padrao.match(informacao)

            # Verificar se houve correspondência
            if correspondencia:
                # Extrair informações específicas
                dados_array = [
                    correspondencia.group(1).strip(),
                    correspondencia.group(2).strip(),
                    correspondencia.group(3).strip(),
                    correspondencia.group(4).strip(),
                    correspondencia.group(5).strip(),
                    correspondencia.group(6).strip(),
                ]

                # Adicionar os dados ao resultado
                self.resultados.append(dados_array)
            else:
                print(f"Não houve correspondência com o padrão para a linha: {linha_dados}")

    def obter_resultados(self):
        return self.resultados
