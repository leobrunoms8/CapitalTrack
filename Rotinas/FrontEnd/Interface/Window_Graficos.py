# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window_Graficos.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window_Graficos(object):
    def setupUi(self, Window_Graficos):
        Window_Graficos.setObjectName("Window_Graficos")
        Window_Graficos.resize(797, 542)
        self.tabWidget = QtWidgets.QTabWidget(Window_Graficos)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 811, 541))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 801, 451))
        self.groupBox.setObjectName("groupBox")
        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView.setGeometry(QtCore.QRect(10, 160, 781, 281))
        self.graphicsView.setObjectName("graphicsView")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit_2.setGeometry(QtCore.QRect(10, 90, 81, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.label_2.setObjectName("label_2")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(10, 40, 81, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Window_Graficos)
        QtCore.QMetaObject.connectSlotsByName(Window_Graficos)

    def retranslateUi(self, Window_Graficos):
        _translate = QtCore.QCoreApplication.translate
        Window_Graficos.setWindowTitle(_translate("Window_Graficos", "Dialog"))
        self.groupBox.setTitle(_translate("Window_Graficos", "Dividendos"))
        self.label_2.setText(_translate("Window_Graficos", "Data Final"))
        self.label.setText(_translate("Window_Graficos", "Data Inicial"))
        self.pushButton.setText(_translate("Window_Graficos", "Exibir Gráfico"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Window_Graficos", "Somátoria de Dividendos por Período"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Window_Graficos", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window_Graficos = QtWidgets.QDialog()
    ui = Ui_Window_Graficos()
    ui.setupUi(Window_Graficos)
    Window_Graficos.show()
    sys.exit(app.exec_())
