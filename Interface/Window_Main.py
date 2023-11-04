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
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.menuArquivo.addAction(self.actionAbrir)
        self.menuArquivo.addAction(self.actionSalvar)
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.actionSair)
        self.menuEditar.addAction(self.actionAdicionar)
        self.menuEditar.addAction(self.actionEditar)
        self.menuEditar.addAction(self.actionExcluir)
        self.menuExibir.addAction(self.actionTela_Cheia)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())
        self.menubar.addAction(self.menuExibir.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
