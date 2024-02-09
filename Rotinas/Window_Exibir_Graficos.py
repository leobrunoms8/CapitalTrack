from matplotlib.backend_bases import FigureCanvasBase
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import yfinance as yf
import mplfinance as mpf

from .FrontEnd.Interface.Window_Graficos import Ui_Window_Graficos

class Window_exibir_Graficos(QDialog):
    def __init__(self, ui_mainwindow):
        super(Window_exibir_Graficos, self).__init__()

        self.ui_mainwindow = ui_mainwindow
        self.ui_graficos = Ui_Window_Graficos()
        self.ui_graficos.setupUi(self)

       

    def exibir_grafico(self):

        self.ui_graficos.pushButton.clicked.connect(self.carregar_grafico)
        self.ui_graficos.pushButton_2.clicked.connect(self.analile_grafica_entre_datas)


        self.show()

    def carregar_grafico(self):
        try:
            data_inicial = self.ui_graficos.dateEdit.date().toString("yyyy-MM-dd")
            data_final = self.ui_graficos.dateEdit_2.date().toString("yyyy-MM-dd")

            datas_consulta = pd.date_range(data_inicial, data_final, freq='D').strftime('%d.%m.%Y').tolist()

            dados_resultado = []
            resultados = []

            
            for data_ex in datas_consulta:
                try:
                    # Conecte ao banco de dados MySQL
                    db = mysql.connector.connect(
                        host="localhost",
                        user="developer",
                        password="Leo140707",
                        database="RaspagemPuraDeDados"
                    )

                    cursor = db.cursor()
                    consulta_sql = f"SELECT valor_dividendo FROM `tabela_{data_ex}`"

                    cursor.execute(consulta_sql)

                    resultados = cursor.fetchall()
                    print(resultados)
                   
                    for tupla in resultados:
                        for item in tupla:
                            # Substituir vírgulas por pontos para garantir que o Python interprete corretamente
                            item_alterado = item.replace(',', '.').replace('(', '').replace(')', '')
                            # Substituir vírgulas por pontos para garantir que o Python interprete corretamente
                            item_corrigido = item_alterado.replace(',', '')
                            # Converter para float
                            numero_float = float(item_corrigido)
                            dados_resultado.append((data_ex, numero_float))


                except Exception as err:
                    print(f"Erro ao processar a data {data_ex}: {err}")
                    continue

            print(dados_resultado)

            # Criando um DataFrame com os dados
            df = pd.DataFrame(dados_resultado, columns=['Data', 'Valor'])

            # Convertendo a coluna 'Data' para o tipo datetime
            df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

            # Agrupando os valores por data e calculando a soma
            df_agrupado = df.groupby('Data')['Valor'].sum().reset_index()

            # Plotando o gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(df_agrupado['Data'], df_agrupado['Valor'], color='blue')
            ax.set_xlabel('Data')
            ax.set_ylabel('Soma do Valor de Dividendo')
            ax.set_title('Soma do Valor de Dividendo por Data')
            plt.xticks(rotation=45)

            # Convertendo o gráfico em um canvas
            canvas = FigureCanvas(fig)

            # Verificando se há um layout definido para a interface gráfica
            if self.ui_graficos.graphicsView.layout() is None:
                # Se não houver, cria um novo layout
                layout = QtWidgets.QVBoxLayout(self.ui_graficos.graphicsView)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(canvas)
            else:
                # Se houver, substitui o widget existente pelo novo canvas
                old_widget = self.ui_graficos.graphicsView.layout().itemAt(0).widget()
                self.ui_graficos.graphicsView.layout().replaceWidget(old_widget, canvas)
                old_widget.close()

            # Desenha o canvas
            canvas.draw()

        except Exception as err:
            print(f"Erro ao processar: {err}")

    def analile_grafica_entre_datas(self):
        
        # Data ex da ação e data ex antecessora
        data_ex = self.ui_graficos.dateEdit_4.date().toString("yyyy-MM-dd")
        data_ex_antecessora = self.ui_graficos.dateEdit_3.date().toString("yyyy-MM-dd")
        print(data_ex)
        print(data_ex_antecessora)

        # Símbolo da ação
        symbol = self.ui_graficos.lineEdit.text()

        # Chamar a função para plotar candlesticks
        self.plot_candlesticks(symbol, data_ex_antecessora, data_ex)
    
    def plot_candlesticks(self, symbol, start_date, end_date):
            # Obter dados históricos do Yahoo Finance
            data = yf.download(symbol, start=start_date, end=end_date)
            
            # Plotar candlesticks usando mplfinance
            mpf.plot(data, type='candle', style='charles', volume=True)

    def grafico_entre_data_ex(self):
        pass