# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dividendos.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dividendos(object):
    def setupUi(self, Dividendos):
        Dividendos.setObjectName("Dividendos")
        Dividendos.resize(677, 534)
        self.tableWidget = QtWidgets.QTableWidget(Dividendos)
        self.tableWidget.setGeometry(QtCore.QRect(0, 70, 671, 421))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.groupBox = QtWidgets.QGroupBox(Dividendos)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 211, 61))
        self.groupBox.setObjectName("groupBox")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.dateEdit.setObjectName("dateEdit")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(100, 20, 101, 21))
        self.pushButton.setObjectName("pushButton")
        self.groupBox.raise_()
        self.tableWidget.raise_()

        self.retranslateUi(Dividendos)
        QtCore.QMetaObject.connectSlotsByName(Dividendos)

    def retranslateUi(self, Dividendos):
        _translate = QtCore.QCoreApplication.translate
        Dividendos.setWindowTitle(_translate("Dividendos", "Dividendos"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dividendos", "Id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dividendos", "Símbolo"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dividendos", "Nome da Epresa"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dividendos", "Data Ex"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dividendos", "Valor do Dividendo"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dividendos", "Data de Pagamento"))
        self.groupBox.setTitle(_translate("Dividendos", "Data Ex"))
        self.pushButton.setText(_translate("Dividendos", "Consultar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dividendos = QtWidgets.QDialog()
    ui = Ui_Dividendos()
    ui.setupUi(Dividendos)
    Dividendos.show()
    sys.exit(app.exec_())
