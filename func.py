import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import pyqtSignal, QObject
# from PyQt5.Qt import QUrl, QImage
from PyQt5.Qt import QPixmap, QImage # 加载图片
from PIL import Image
import socket

from test import Ui_MainWindow

IMAGE = '1'
TEXT = '2'
PAR_ERR = 1

class Function(Ui_MainWindow, QMainWindow):
    __setSock = pyqtSignal(str)

    def __init__(self):
        '''
        self.__state 记录服务状态
        self.__IP 记录IP
        self.__port 记录Port
        self.__Sock 保存服务
        self.__path 保存图片路径
        self.__busy 标记是否正在工作
        self.__errTimes 记录传输或接受过程中的错误次数
        '''
        super(Function,self).__init__()
        self.setupUi(self)

        self.__state = None
        self.__IP = None
        self.__port = None
        self.__Sock = None
        self.__path = None
        self.__busy = False
        self.__errTimes = 0

        self.conButton.cliked.connect(self.__setConn)
        self.disButton.clicked.connect(self.__disConn)
        self.restButton.clicked.connect(self.__clear)
        self.cli_but.clicked.connect(self.__setClient)
        self.ser_but.clicked.connect(self.__setServe)
        self.setGraph.clicked.connect(self.__selectGraph)

    def __statsErr(self):
        # 没有选 客户端 或 服务端 的错误信息
        QMessageBox.information(self, "State has not init", "Please Choose Server or Client")

    def __AddErr(self):
        # 地址输入错误 的提示信息
        QMessageBox.information(self, "InValid Add or Port", "Please type in a correct Address and Port")

    def __conErr(self):
        # 没建立连接 的提示信息信息
        QMessageBox.information(self,"Connection Error", "No Connection")

    def __timeOutErr(self):
        # 联接超时 的提示信息
        pass

    def __clear(self):
        # 清空输入
        self.Add.setText('')
        self.Port.setText('')

    def __setConn(self):
        # 检测是否设置了 IP 与 port
        if self.Add.text() == None or self.Port.text() == None :
            self.__AddErr()
        else :
            self.__IP = self.Add.text()
            self.__port = self.Port.text()

        # 检测是否选择了 服务类型
        if self.__state == None:
            self.__statsErr()
            return
        if self.__state == 'Serve' : # 设为 服务端
            try:
                self.__Sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.__Sock.bind((self.__IP, self.__port))
                self.__Sock.listen(1)  # 先随便设一个 应该没问题
                self.textDisp.setText("Serve start successfully! \n Waiting for connection.....\n")

            except:
                QMessageBox.warning(self, 'Connection Error',
                                    'Can not set Connection \n check whether you IP and Port is Valid')
                self.__Sock.shutdown(2)
                self.__Sock.close()
                self.__Sock = None

        else :  # 设为 客户端
            self.cli_but.setDisabled(True)
            self.ser_but.setDisabled(True)

            pass

    def __serSock(self):
        # 服务端工作开始
        while True:
            conn, add = self.__Sock.accept()
            self.textDisp.append('Get connection from', add[0], ':', add[1])
            while True:

                kind = conn.decode()

                pass
        pass

    def __disConn(self, state):
        #  断开链接
        if self.__Sock == None : # 未建立连接
            return

        button = QMessageBox.information(self, 'Interrupt Serve', 'Are you sure to interrupt the serve?',
                                         QMessageBox.Ok | QMessageBox.No)
        if button == QMessageBox.Ok:
            self.__state = state
            self.__busy = False
            self.__Sock.shutdown(2)
            self.__Sock.close()
            self.__Sock = None
            self.textDisp.setText("Connection Interrupt!\n")
            self.__IP = None
            self.__port = None
            self.cli_but.setDisabled(True)
            self.ser_but.setDisabled(True)

    def __setClient(self):
        # 设置状态为 客户端
        if self.__state == None  or self.__state == 'Serve' :
            self.__state = "Client"

    def __setServe(self):
        # 设置状态为 服务端
        if self.__state == None or self.__state == 'Client' :
            self.__state = "Serve"

    def __selectGraph(self):
        # 预览与展示
        self.__path = QFileDialog.getOpenFileName(self, "Select Graph", "","Image(*.jpg)")[0]
        self.__showGraph()

    def __showGraph(self):
        self.graphDisp.setPixmap(QPixmap.fromImage(QImage(self.__path)))

    def __parCont(self, cont):
        '''
        input:
            cont: python bytes 类型 需要decode 得到字符串
        '''
        kind = cont.decode()
        if kind == IMAGE : # IMAGE
            return
            pass
        elif kind == TEXT :
            pass
        else: # 无法接续 报错
            self.__errTimes += 1
            pass

    def __sendError(self, kind):
        '''
        向另一端发送错误信息 错误类型
        input:
            kind: int类型 表示错误类型
        '''

        pass

    def __sendGraph(self):
        if self.__Sock == None:
            pass

    def __sendText(self):
        if self.__Sock == None :
            pass