import mysql.connector
import yfinance as yf
from Relação_Dividendo_Acao import CalculadoraDividendos

# Função para obter o preço atual da ação usando a API yfinance
def obter_preco_acao(simbolo):
    try:
        acao = yf.Ticker(simbolo)
        historico = acao.history(period='1d')
        preco_atual = float(historico['Close'].iloc[-1])  # Obtém o preço de fechamento mais recente
        return preco_atual
    except Exception as e:
        print(f"Erro ao obter preço da ação {simbolo}: {e}")
        return None

# Função principal para processar a tabela no banco de dados MySQL
def processar_tabela_mysql(nome_tabela, simbolo_acao, conexao):
    cursor = conexao.cursor()

    # Consultar o valor_dividendo da tabela
    query = f"SELECT valor_dividendo FROM `{nome_tabela}` WHERE simbolo = '{simbolo_acao}'"
    cursor.execute(query)
    resultado = cursor.fetchone()

    if resultado:
        valor_dividendo_tabela = resultado[0]

        # Converta o valor_dividendo para float
        try:
            valor_dividendo_tabela = float(valor_dividendo_tabela.replace(',', '.'))
        except ValueError:
            print(f"Erro ao converter valor_dividendo para float para '{simbolo_acao}' na tabela '{nome_tabela}'")
            cursor.close()
            return

        preco_acao = obter_preco_acao(simbolo_acao)

        if preco_acao is not None:
            # Função para calcular a relação entre o valor da ação e o dividendo
            calculadora = CalculadoraDividendos()
            calculadora.configurar_valores(preco_acao, valor_dividendo_tabela)
            relacao_dividendo = calculadora.calcular_relacao_dividendo()
            

            if relacao_dividendo is not None:
                print(f"Cada ação do '{simbolo_acao}' vale '{preco_acao}' e pagará '{valor_dividendo_tabela}' de dividendos, o que equivale a '{relacao_dividendo}' por real investido")
            else:
                print(f"Não foi possível calcular a relação entre o valor da ação e o dividendo para '{simbolo_acao}'")
        else:
            print(f"Não foi possível obter o preço da ação para '{simbolo_acao}'")
    else:
        print(f"Símbolo '{simbolo_acao}' não encontrado na tabela '{nome_tabela}'")

    cursor.close()

# Substitua esses valores pelos detalhes do seu banco de dados
host = "localhost"
usuario = "developer"
senha = "Leo140707"
banco_de_dados = "RaspagemPuraDeDados"

# Conectar ao banco de dados
conexao = mysql.connector.connect(
    host=host,
    user=usuario,
    password=senha,
    database=banco_de_dados
)

# Exemplo de uso
tabela_nome = "tabela_04.12.2023"
simbolo_acao = "BBDO"  # Substitua pelo símbolo real da ação

# Remova o argumento 'valor_dividendo' se não for necessário
processar_tabela_mysql(tabela_nome, simbolo_acao, conexao)


# Fechar a conexão após o uso
conexao.close()
