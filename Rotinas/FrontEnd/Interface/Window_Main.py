# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window_Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(829, 624)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 801, 451))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 829, 21))
        self.menubar.setObjectName("menubar")
        self.menuArquivo = QtWidgets.QMenu(self.menubar)
        self.menuArquivo.setObjectName("menuArquivo")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuExibir = QtWidgets.QMenu(self.menubar)
        self.menuExibir.setObjectName("menuExibir")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionSalvar = QtWidgets.QAction(MainWindow)
        self.actionSalvar.setObjectName("actionSalvar")
        self.actionAdicionar = QtWidgets.QAction(MainWindow)
        self.actionAdicionar.setObjectName("actionAdicionar")
        self.actionEditar = QtWidgets.QAction(MainWindow)
        self.actionEditar.setObjectName("actionEditar")
        self.actionExcluir = QtWidgets.QAction(MainWindow)
        self.actionExcluir.setObjectName("actionExcluir")
        self.actionTela_Cheia = QtWidgets.QAction(MainWindow)
        self.actionTela_Cheia.setObjectName("actionTela_Cheia")
        self.actionSair = QtWidgets.QAction(MainWindow)
        self.actionSair.setObjectName("actionSair")
        self.actionListas = QtWidgets.QAction(MainWindow)
        self.actionListas.setObjectName("actionListas")
        self.actionDividendos = QtWidgets.QAction(MainWindow)
        self.actionDividendos.setObjectName("actionDividendos")
        self.menuArquivo.addAction(self.actionAbrir)
        self.menuArquivo.addAction(self.actionSalvar)
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.actionSair)
        self.menuEditar.addAction(self.actionAdicionar)
        self.menuEditar.addAction(self.actionEditar)
        self.menuEditar.addAction(self.actionExcluir)
        self.menuExibir.addAction(self.actionTela_Cheia)
        self.menuExibir.addAction(self.actionListas)
        self.menuExibir.addAction(self.actionDividendos)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuExibir.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Dividendos"))
        self.label_2.setText(_translate("MainWindow", "Data Final"))
        self.label.setText(_translate("MainWindow", "Data Inicial"))
        self.pushButton.setText(_translate("MainWindow", "Exibir Gráfico"))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuExibir.setTitle(_translate("MainWindow", "Exibir"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionSalvar.setText(_translate("MainWindow", "Salvar"))
        self.actionAdicionar.setText(_translate("MainWindow", "Adicionar..."))
        self.actionEditar.setText(_translate("MainWindow", "Editar..."))
        self.actionExcluir.setText(_translate("MainWindow", "Excluir..."))
        self.actionTela_Cheia.setText(_translate("MainWindow", "Tela Cheia"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))
        self.actionListas.setText(_translate("MainWindow", "Listas"))
        self.actionDividendos.setText(_translate("MainWindow", "Dividendos"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())