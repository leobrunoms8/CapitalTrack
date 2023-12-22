from PyQt5.QtCore import QDate
from datetime import datetime

# Suponha que data_inicial e data_final sejam strings no formato "dd.MM.yyyy"
data_inicial = "04.12.2023"
data_final = "28.12.2023"

# Converter as strings para objetos QDate
qdate_inicial = QDate.fromString(data_inicial, "dd.MM.yyyy")
qdate_final = QDate.fromString(data_final, "dd.MM.yyyy")

# Obter as datas como objetos datetime
data_inicial_datetime = datetime(qdate_inicial.year(), qdate_inicial.month(), qdate_inicial.day())
data_final_datetime = datetime(qdate_final.year(), qdate_final.month(), qdate_final.day())

# Converter as datas para o formato "MM.dd.yyyy"
data_inicial_formatada = data_inicial_datetime.strftime("%m.%d.%Y")
data_final_formatada = data_final_datetime.strftime("%m.%d.%Y")

# Imprimir os resultados
print("Data Inicial formatada:", data_inicial_formatada)
print("Data Final formatada:", data_final_formatada)
