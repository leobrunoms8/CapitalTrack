# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window_Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window_Login(object):
    def setupUi(self, Window_Login):
        Window_Login.setObjectName("Window_Login")
        Window_Login.resize(476, 272)
        self.Window_Login_Password = QtWidgets.QLineEdit(Window_Login)
        self.Window_Login_Password.setGeometry(QtCore.QRect(70, 190, 121, 20))
        self.Window_Login_Password.setFrame(False)
        self.Window_Login_Password.setObjectName("Window_Login_Password")
        self.Window_Login_User = QtWidgets.QLineEdit(Window_Login)
        self.Window_Login_User.setGeometry(QtCore.QRect(70, 150, 121, 20))
        self.Window_Login_User.setFrame(False)
        self.Window_Login_User.setObjectName("Window_Login_User")
        self.Background_Login = QtWidgets.QLabel(Window_Login)
        self.Background_Login.setGeometry(QtCore.QRect(0, -80, 481, 441))
        self.Background_Login.setStyleSheet("image: url(:/newPrefix/Canva/Login_Backgound_002.png);")
        self.Background_Login.setText("")
        self.Background_Login.setObjectName("Background_Login")
        self.Background_Login.raise_()
        self.Window_Login_Password.raise_()
        self.Window_Login_User.raise_()

        self.retranslateUi(Window_Login)
        QtCore.QMetaObject.connectSlotsByName(Window_Login)

    def retranslateUi(self, Window_Login):
        _translate = QtCore.QCoreApplication.translate
        Window_Login.setWindowTitle(_translate("Window_Login", "Dialog"))
        self.Window_Login_Password.setPlaceholderText(_translate("Window_Login", "Digite a Senha"))
        self.Window_Login_User.setPlaceholderText(_translate("Window_Login", "Digite o seu Usuario"))
import Backgtound_Login_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window_Login = QtWidgets.QDialog()
    ui = Ui_Window_Login()
    ui.setupUi(Window_Login)
    Window_Login.show()
    sys.exit(app.exec_())