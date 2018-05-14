import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.Qt import QUrl, QImage

from test import Ui_MainWindow

class Function(Ui_MainWindow, QMainWindow):
    _signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(Function,self).__init__()
        self.setupUi(self)
        self.but_change_str.clicked.connect(self.change_str)
        self.button_emit1.clicked.connect(self.send_mes)
        self._signal.connect(self.plus_one)
        pass

    def change_str(self):
        self.textBrowser.setText("text has changed!")

        self.textBrowser.append("Finished!!!")

    def send_mes(self):
        self._signal.emit("haha?")
        pass

    def plus_one(self):
        self.textBrowser.setText("-------    --------")
        self.textBrowser.append( "|     /    \\     |")
        self.textBrowser.append( "|    /------\\    |")
        self.textBrowser.append( "|   /        \\   |")
        self.textBrowser.append( "----          -----")
