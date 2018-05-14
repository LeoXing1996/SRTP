# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(866, 648)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(160, 30, 481, 311))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_click = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.button_click.setFont(font)
        self.button_click.setObjectName("button_click")
        self.horizontalLayout.addWidget(self.button_click)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_emit1 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_emit1.setObjectName("button_emit1")
        self.gridLayout.addWidget(self.button_emit1, 1, 0, 1, 1)
        self.button_emit2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_emit2.setObjectName("button_emit2")
        self.gridLayout.addWidget(self.button_emit2, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.but_change_str = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.but_change_str.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.but_change_str.setObjectName("but_change_str")
        self.horizontalLayout.addWidget(self.but_change_str)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(159, 369, 481, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 866, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.button_click.clicked.connect(self.but_change_str.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_click.setText(_translate("MainWindow", "click"))
        self.button_emit1.setText(_translate("MainWindow", "+1"))
        self.button_emit2.setText(_translate("MainWindow", "PushButton"))
        self.but_change_str.setText(_translate("MainWindow", "setText"))

