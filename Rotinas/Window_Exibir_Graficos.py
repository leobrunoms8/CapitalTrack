from matplotlib.backend_bases import FigureCanvasBase
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from sqlalchemy import create_engine

from .FrontEnd.Interface.Window_Graficos import Ui_Window_Graficos

class Window_exibir_Graficos(QDialog):
    def __init__(self, ui_mainwindow):
        super(Window_exibir_Graficos, self).__init__()

        self.ui_mainwindow = ui_mainwindow
        self.ui_graficos = Ui_Window_Graficos()
        self.ui_graficos.setupUi(self)

        self.ui_graficos.pushButton.clicked.connect(self.exibir_grafico)

    def exibir_grafico(self):
        self.show()

        try:
            engine = create_engine("mysql+pymysql://developer:Leo140707@localhost/raspagempuradedados")

            data_inicial = self.ui_graficos.dateEdit.date().toString("dd.MM.yyyy")
            data_final = self.ui_graficos.dateEdit_2.date().toString("dd.MM.yyyy")

            datas_consulta = pd.date_range(data_inicial, data_final, freq='D').strftime('%d.%m.%Y').tolist()

            dados_resultado = []

            with engine.connect() as conexao:
                for data_ex in datas_consulta:
                    try:
                        tabela_existe = self.verificar_tabela_existente(conexao, data_ex)

                        if tabela_existe:
                            consulta_sql = f"SELECT data_ex, SUM(CAST(REPLACE(valor_dividendo, ',', '.') AS DECIMAL(10, 4))) as soma_valor_dividendo " \
                                           f"FROM `tabela_{data_ex}` GROUP BY data_ex"

                            resultados = conexao.execute(consulta_sql).fetchall()

                            if not resultados:
                                print(f"Nenhum dado encontrado para a tabela_{data_ex}")
                                continue

                            for resultado in resultados:
                                dados_resultado.append({'data': resultado[0], 'soma_valor_dividendo': resultado[1]})

                    except Exception as err:
                        print(f"Erro ao processar a data {data_ex}: {err}")
                        continue

            resultado_df = pd.DataFrame(dados_resultado)
            resultado_df['data'] = resultado_df['data'].replace('--', np.nan)
            resultado_df['data'] = pd.to_datetime(resultado_df['data'], format='%d.%m.%Y', errors='coerce')
            resultado_df = resultado_df.sort_values(by='data')

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(resultado_df['data'], resultado_df['soma_valor_dividendo'])
            ax.set_xlabel('Data Ex')
            ax.set_ylabel('Soma do Valor de Dividendo')
            ax.set_title('Soma do Valor de Dividendo por Data EX')
            plt.xticks(rotation=45)

            canvas = FigureCanvasBase(fig)

            if self.ui_graficos.graphicsView.layout() is None:
                layout = QtWidgets.QVBoxLayout(self.ui_dividendos.graphicsView)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(canvas)
            else:
                old_widget = self.ui_graficos.graphicsView.layout().itemAt(0).widget()
                self.ui_graficos.graphicsView.layout().replaceWidget(old_widget, canvas)
                old_widget.close()

            canvas.draw()

        except Exception as e:
            print(f"Erro ao exibir gráfico: {e}")

    def verificar_tabela_existente(self, conexao, data_ex):
        try:
            result = conexao.execute(f"SHOW TABLES LIKE 'tabela_{data_ex}'")
            return result.fetchone() is not None
        except Exception as err:
            print(f"Erro ao verificar a existência da tabela tabela_{data_ex}: {err}")
            return False
